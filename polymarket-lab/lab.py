"""
Polymarket strategy lab: one run.

Pretend money only. Public data, no account, no keys, no orders.

Each run (every 40 minutes, inside the "Bots - every 40 minutes" workflow):
1. Settles pretend positions whose markets have resolved ($1 or $0 a share).
2. Lists every open event that ends within 7 days (Gamma; about 7,500
   events holding 100,000+ markets, mostly sports props).
3. Asks each strategy in strategies.py which markets it would buy.
4. Fills those buys against the real order book (walking the asks, up to
   the strategy's price cap) and adds Polymarket's taker fee. A fill below
   Polymarket's minimum order (usually 5 shares) is no trade.
5. Daily temperature markets: compares each range's price with the chance
   two weather-model ensembles give it, and buys where the forecast gives
   at least 10 cents more than the price, before the station's local day
   starts ("weather_forecast", see weather.py).
6. Looks for multi-choice markets whose prices add up to less than $1
   ("price_gap"), and fills those against the real books too.
7. Rewrites report.md / summary.json.

Data layout (the polymarket-lab-data branch):
- state.json: open positions, which events each strategy already traded,
  stored verdicts and station coordinates
- forecasts_cache.json: each station's latest weather-model ensemble
- trades/YYYY-MM.jsonl: every pretend buy, one per line
- settled/YYYY-MM.jsonl: every finished position with its result
- runs.jsonl: when each run happened, how long it took, and any problems
- gaps/YYYY-MM-DD.jsonl: each near price gap seen by price_gap
- weather/YYYY-MM-DD.jsonl: each forecast-versus-price disagreement found
- forecasts/YYYY-MM-DD.jsonl: one full forecast-versus-price snapshot per
  temperature event per day, for checking calibration later
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.append(str(HERE.parent / "polymarket-shadow"))
import pmapi  # noqa: E402  (shared read-only API helpers)

import report  # noqa: E402
import strategies as S  # noqa: E402
import weather  # noqa: E402

HORIZON_HOURS = 168
SLICE_HOURS = 6  # Gamma refuses offsets past about 2,000; slices that still overflow are halved
MIN_SLICE_SECONDS = 600
MAX_LIST_CALLS = 400
MAX_FAILED_SLICES = 6  # more failed slice reads than this in one run: Gamma is down, stop
# What a strategy gets to see of a market (the rest of Gamma's record is dropped to save memory)
VIEW_KEYS = ("conditionId", "question", "groupItemTitle", "bestBid", "bestAsk", "oneDayPriceChange", "negRisk",
             "negRiskAugmented", "endDate", "sportsMarketType", "gameStartTime", "orderMinSize", "volume24hr")
GAP_BUDGET_USD = 20.0  # most a price_gap trade may spend
GAP_MIN_EDGE = 0.005  # needs at least half a cent a share-set after fees
GAP_MAX_OUTCOMES = 40
GAP_NEAR = 0.02  # a set within 2% of its payout is worth looking at (and recording)
GAP_MAX_EVENTS = 60  # most events whose books are read in one run (the nearest gaps first)
STALE_DAYS = 3  # an open position this long past its market's end is reported
REMEMBER_DAYS = 7  # how long after its end an event stays "already traded"


def parse_ts(s: str | None) -> float | None:
    if not s:
        return None
    s = s.strip().replace(" ", "T").replace("Z", "+00:00")
    if s.endswith("+00"):
        s += ":00"
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.timestamp()


def _json_list(v) -> list:
    if isinstance(v, list):
        return v
    try:
        out = json.loads(v or "[]")
        return out if isinstance(out, list) else []
    except (TypeError, ValueError):
        return []


def _float(x, default: float) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def market_view(m: dict, now: float) -> dict | None:
    """Gamma market plus the fields strategies use; None if it cannot be traded."""
    end = parse_ts(m.get("endDate"))
    tokens = [str(t) for t in _json_list(m.get("clobTokenIds"))]
    if end is None or len(tokens) != 2 or not m.get("conditionId"):
        return None
    if m.get("closed") or not m.get("active") or m.get("acceptingOrders") is False or m.get("enableOrderBook") is False:
        return None
    v = {k: m.get(k) for k in VIEW_KEYS}
    v["ends_at"] = int(end)
    v["hours_left"] = (end - now) / 3600
    v["sport"] = m.get("sportsMarketType") or None
    start = parse_ts(m.get("gameStartTime"))
    v["hours_to_start"] = (start - now) / 3600 if start else None
    v["tokens"] = tokens
    v["outcomes"] = _json_list(m.get("outcomes"))
    ev = (m.get("events") or [{}])[0] or {}
    v["event_id"] = str(ev.get("id") or m["conditionId"])
    v["event_title"] = ev.get("title") or m.get("question")
    v["temp"] = weather.is_temperature_event(v["event_title"])
    v["volume_24h"] = _float(m.get("volume24hr"), 0.0)
    v["min_size"] = _float(m.get("orderMinSize"), 5.0) or 5.0
    sched = m.get("feeSchedule") or {}
    v["fee_rate"] = float(sched.get("rate") or 0) if m.get("feesEnabled") else 0.0
    v["fee_exp"] = float(sched.get("exponent") or 1)
    return v


def fee(shares: float, price: float, rate: float, exp: float = 1.0) -> float:
    """Polymarket's taker fee: shares * rate * (p * (1 - p)) ** exponent."""
    return shares * rate * (price * (1 - price)) ** exp if rate > 0 else 0.0


def asks_of(book: dict | None) -> list[tuple[float, float]]:
    out = []
    for lvl in (book or {}).get("asks") or []:
        try:
            p, s = float(lvl["price"]), float(lvl["size"])
        except (KeyError, TypeError, ValueError):
            continue
        if 0 < p < 1 and s > 0:
            out.append((p, s))
    return sorted(out)


def fill_dollars(asks, budget: float, cap: float, rate: float, exp: float = 1.0):
    """Buy up to `budget` dollars (fees included) at prices <= cap. Returns (shares, cost)."""
    shares = cost = 0.0
    for p, s in asks:
        if p > cap + 1e-9:
            break
        unit = p + fee(1, p, rate, exp)
        take = min(s, (budget - cost) / unit)
        if take <= 0:
            break
        shares += take
        cost += take * unit
        if budget - cost < 1e-6:
            break
    return shares, cost


def fill_shares(asks, shares: float, rate: float, exp: float = 1.0):
    """Cost (fees included) of exactly `shares`, or None if the book is too thin."""
    left, cost = shares, 0.0
    for p, s in asks:
        take = min(s, left)
        cost += take * (p + fee(1, p, rate, exp))
        left -= take
        if left <= 1e-9:
            return cost
    return None


# ---------------------------------------------------------------- data access

def _event_slice(a: float, b: float, fetch) -> tuple[list[dict], bool, int]:
    """Events ending in [a, b): (rows, complete, calls). Incomplete when Gamma's offset cap was hit."""
    rows: list[dict] = []
    offset, calls = 0, 0
    while True:
        q = urllib.parse.urlencode({
            "active": "true", "closed": "false", "limit": 100, "offset": offset,
            "end_date_min": dt.datetime.fromtimestamp(a, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_date_max": dt.datetime.fromtimestamp(b, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
        page = fetch(f"{pmapi.GAMMA}/events?{q}", None)
        calls += 1
        if not isinstance(page, list):
            raise pmapi.ApiError("/events: unexpected shape")
        rows.extend(page)
        if len(page) < 100:
            return rows, True, calls
        offset += 100
        if offset > 2000:
            return rows, False, calls


def list_events(now: float, fetch=pmapi.http_json) -> tuple[list[dict], list[str]]:
    """
    Every open event ending within HORIZON_HOURS, with its markets, and any
    problems. (Events, not markets: a week holds 100,000+ markets but only
    about 7,500 events, and Gamma pages at 100 a call.) The week is read in
    SLICE_HOURS slices, several at once; a slice with more events than Gamma
    will page through is split in half until it fits (or is MIN_SLICE_SECONDS
    long, when the rest of it is given up and reported). A slice whose call
    fails is tried once more and then given up and reported, so one Gamma
    hiccup does not cost the whole week; many failures mean Gamma is down,
    and then the listing fails as a whole.
    """
    problems: list[str] = []
    out: list[dict] = []
    calls = 0
    retried: set[tuple[float, float]] = set()
    failed: list[str] = []
    failures = 0
    last_error = ""
    pending = []
    a = now
    while a < now + HORIZON_HOURS * 3600:
        b = min(a + SLICE_HOURS * 3600, now + HORIZON_HOURS * 3600)
        pending.append((a, b))
        a = b
    while pending:
        if calls > MAX_LIST_CALLS:
            problems.append(f"events: stopped after {calls} calls with {len(pending)} slices unread")
            break
        batch, pending = pending[:16], pending[16:]
        results = pmapi.parallel({f"{a}-{b}": (lambda a=a, b=b: _event_slice(a, b, fetch)) for a, b in batch}, workers=8)
        for (a, b), res in zip(batch, results.values()):
            if isinstance(res, Exception):
                calls += 1
                failures += 1
                last_error = str(res) if isinstance(res, pmapi.ApiError) else repr(res)
                if failures > MAX_FAILED_SLICES:
                    raise pmapi.ApiError(f"{failures} slice reads failed, Gamma seems down: {last_error}"[:300])
                if (a, b) not in retried:
                    retried.add((a, b))
                    pending.append((a, b))
                else:
                    failed.append(dt.datetime.fromtimestamp(a, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"))
                continue
            rows, complete, n = res
            calls += n
            if complete:
                out.extend(rows)
            elif b - a > MIN_SLICE_SECONDS:
                mid = (a + b) / 2
                pending += [(a, mid), (mid, b)]
            else:
                out.extend(rows)
                when = dt.datetime.fromtimestamp(a, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
                problems.append(f"events: more than {len(rows)} events end around {when} UTC; the rest were not read")
    if failed:
        problems.append(f"events: {len(failed)} slice(s) could not be read twice (from {failed[0]} UTC): "
                        f"{last_error}"[:300])
    seen, uniq = set(), []
    for ev in out:
        if ev.get("id") not in seen:
            seen.add(ev.get("id"))
            uniq.append(ev)
    return uniq, problems


def markets_of(events: list[dict]):
    """The events' markets (in place), each knowing its event (id, title, negRiskAugmented)."""
    for ev in events:
        for m in ev.get("markets") or []:
            if not isinstance(m, dict):
                continue
            m.setdefault("events", [{"id": ev.get("id"), "title": ev.get("title")}])
            if ev.get("negRiskAugmented") and m.get("negRiskAugmented") is None:
                m["negRiskAugmented"] = True
            yield m


def closed_markets(condition_ids, fetch=pmapi.http_json) -> dict[str, dict]:
    ids = list(condition_ids)
    out: dict[str, dict] = {}
    for i in range(0, len(ids), 20):
        q = "&".join(f"condition_ids={c}" for c in ids[i:i + 20])
        rows = fetch(f"{pmapi.GAMMA}/markets?closed=true&limit=20&{q}", None)
        for r in rows if isinstance(rows, list) else []:
            if r.get("conditionId"):
                out[r["conditionId"]] = r
    return out


# ---------------------------------------------------------------- settlement

def final_prices(m: dict) -> list[float] | None:
    if not m.get("closed"):
        return None
    try:
        prices = [float(x) for x in _json_list(m.get("outcomePrices"))]
    except (TypeError, ValueError):
        return None
    if len(prices) != 2 or any(p not in (0.0, 0.5, 1.0) for p in prices) or abs(sum(prices) - 1) > 1e-9:
        return None
    return prices


def settle(state: dict, now: float, fetch=pmapi.http_json) -> list[dict]:
    open_pos = state["positions"]
    ids = {leg["condition_id"] for p in open_pos for leg in p["legs"]}
    if not ids:
        return []
    closed = closed_markets(ids, fetch)
    done, keep = [], []
    for p in open_pos:
        payout = 0.0
        finished = True
        for leg in p["legs"]:
            prices = final_prices(closed.get(leg["condition_id"]) or {})
            if prices is None:
                finished = False
                break
            payout += leg["shares"] * prices[leg["outcome_index"]]
        if not finished:
            keep.append(p)
            continue
        p = dict(p, payout=round(payout, 6), pnl=round(payout - p["cost"], 6),
                 settled_at=int(now), won=payout > p["cost"])
        done.append(p)
    state["positions"] = keep
    return done


# ---------------------------------------------------------------- entries

FOREVER = 4_102_444_800  # 2100-01-01: the expiry given to first-version entries, which had none


def _traded(state: dict, name: str) -> set:
    """Event ids `name` has already bought. Stored as {event_id: forget_after_ts}."""
    cur = state["traded_events"].get(name)
    if isinstance(cur, list):  # the first version kept a plain list
        cur = {str(eid): FOREVER for eid in cur}
    cur = cur if isinstance(cur, dict) else {}
    state["traded_events"][name] = cur
    return set(cur)


def pick_entries(views: list[dict], state: dict, rng: random.Random) -> dict[str, list]:
    picks: dict[str, list] = {}
    for name, cfg in S.STRATEGIES.items():
        if not cfg.get("active") or cfg.get("rule") is None:
            continue
        traded = _traded(state, name)
        cands, events = [], set()
        for v in views:
            if v["event_id"] in traded or v["event_id"] in events:
                continue
            hit = cfg["rule"](v, rng)
            if hit:
                cands.append((v, hit[0], hit[1], None))
                events.add(v["event_id"])
        rng.shuffle(cands)
        picks[name] = cands[: S.MAX_NEW_PER_RUN]
    return picks


def make_trade(name: str, v: dict, idx: int, cap: float, book: dict | None, now: float, note: dict | None = None) -> dict | None:
    shares, cost = fill_dollars(asks_of(book), S.STAKE_USD, cap, v["fee_rate"], v["fee_exp"])
    if cost < 1.0 or shares < v["min_size"] - 1e-9:  # below Polymarket's smallest order: no real trade possible
        return None
    return {
        **({"note": note} if note else {}),
        "strategy": name, "opened_at": int(now), "event_id": v["event_id"], "ends_at": v["ends_at"],
        "title": (v.get("question") or "")[:140], "event": (v.get("event_title") or "")[:140],
        "sport": v["sport"], "hours_left": round(v["hours_left"], 2),
        "cost": round(cost, 6), "avg_price": round(cost / shares, 6), "payout_if_won": round(shares, 6),
        "legs": [{"condition_id": v["conditionId"], "outcome_index": idx,
                  "outcome": (v["outcomes"][idx] if idx < len(v["outcomes"]) else str(idx)),
                  "shares": round(shares, 6)}],
    }


def price_gap_trades(views: list[dict], events_by_id: dict, state: dict, now: float, fetch=pmapi.http_json) -> tuple[list[dict], list[dict]]:
    """
    In a multi-choice ("neg-risk") event exactly one choice wins. If buying
    every Yes costs less than $1 a set, or every No less than (n-1) dollars,
    the difference is locked in. Returns (trades, sightings).

    Events Polymarket may still add choices to ("negRiskAugmented") are
    skipped on the Yes side: a later-added winner would make every held Yes
    worth nothing, so that payout is not locked in.
    """
    by_event: dict[str, list[dict]] = {}
    for v in views:
        if v.get("negRisk"):
            by_event.setdefault(v["event_id"], []).append(v)
    traded = _traded(state, "price_gap")
    trades, sightings = [], []
    near = []
    for eid, ms in by_event.items():
        if eid in traded or len(ms) < 2 or len(ms) > GAP_MAX_OUTCOMES:
            continue
        asks = [_float(m.get("bestAsk"), -1.0) for m in ms]
        bids = [_float(m.get("bestBid"), 0.0) for m in ms]  # no bid at all: that choice's No cannot be bought below $1
        if any(a < 0 for a in asks):
            continue  # a choice with no ask at all: no full Yes set to buy
        yes_sum, no_sum = sum(asks), sum(1 - max(b, 0.0) for b in bids)
        ratio = min(yes_sum, no_sum / (len(ms) - 1))  # cost of the cheaper full set per dollar it pays, by Gamma's quotes
        if ratio >= 1.0 - GAP_NEAR:
            continue  # nothing near a gap on either side; skip the book calls
        near.append((ratio, eid, ms))
    near.sort(key=lambda x: x[0])
    for ratio, eid, ms in near[:GAP_MAX_EVENTS]:
        ev = events_by_id.get(eid)
        legs_src = [market_view(m, now) for m in (ev or {}).get("markets") or []]
        if not ev or any(x is None for x in legs_src) or len(legs_src) != len(ms):
            continue  # a closed, paused or unlisted choice: not a complete set
        augmented = bool(ev.get("negRiskAugmented") or any(m.get("negRiskAugmented") for m in ms))
        try:
            books = pmapi.books([t for x in legs_src for t in x["tokens"]], fetch)
        except pmapi.ApiError:
            continue
        min_size = max(x["min_size"] for x in legs_src)
        for side, payout_per_set in ((0, 1.0), (1, float(len(legs_src) - 1))):
            if side == 0 and augmented:
                continue
            books_side = [asks_of(books.get(x["tokens"][side])) for x in legs_src]
            best = None
            k = float(min_size)
            while True:
                costs = [fill_shares(b, k, x["fee_rate"], x["fee_exp"]) for b, x in zip(books_side, legs_src)]
                if any(c is None for c in costs):
                    break
                total = sum(costs)
                if total > GAP_BUDGET_USD or payout_per_set * k - total < GAP_MIN_EDGE * k:
                    break
                best = (k, total, costs)
                k += 1.0
            first = [fill_shares(b, float(min_size), x["fee_rate"], x["fee_exp"]) for b, x in zip(books_side, legs_src)]
            if all(c is not None for c in first) and sum(first) / min_size <= payout_per_set * (1 + GAP_NEAR):
                sightings.append({"event_id": eid, "event": ev.get("title"), "side": "yes" if side == 0 else "no",
                                  "n": len(legs_src), "cost_per_set": round(sum(first) / min_size, 4),
                                  "pays": payout_per_set, "augmented": augmented, "at": int(now)})
            if best:
                k, total, costs = best
                trades.append({
                    "strategy": "price_gap", "opened_at": int(now), "event_id": eid,
                    "ends_at": max(x["ends_at"] for x in legs_src),
                    "title": f"All {'Yes' if side == 0 else 'No'} on: {(ev.get('title') or '')[:110]}",
                    "event": (ev.get("title") or "")[:140], "sport": None, "hours_left": round(legs_src[0]["hours_left"], 2),
                    "cost": round(total, 6), "avg_price": round(total / k, 6), "payout_if_won": round(payout_per_set * k, 6),
                    "legs": [{"condition_id": x["conditionId"], "outcome_index": side,
                              "outcome": x.get("groupItemTitle") or x.get("question"), "shares": k} for x in legs_src],
                })
                break  # one side per event
    return trades, sightings


# ---------------------------------------------------------------- run

def load_state(data: Path) -> dict:
    f = data / "state.json"
    if f.exists():
        st = json.loads(f.read_text())
    else:
        st = {}
    st.setdefault("positions", [])
    st.setdefault("traded_events", {})
    st.setdefault("verdicts", {})
    for name in list(st["traded_events"]):  # first-version lists become {event_id: forget_after_ts} once
        _traded(st, name)
    return st


def append_jsonl(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    """Write through a temporary file and a rename, so a kill mid-write never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def _month(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m")


def run(data: Path, now: float | None = None, fetch=pmapi.http_json, seed: int | None = None) -> dict:
    """
    One run. Whatever goes wrong, the run's row, the state and the report
    are written before the error is raised again, so a crash is visible in
    runs.jsonl and never settles or buys anything twice.
    """
    now = time.time() if now is None else now
    t0 = time.time()
    data.mkdir(parents=True, exist_ok=True)
    state = load_state(data)
    cache_file = data / "forecasts_cache.json"
    cache_before = cache_file.read_text() if cache_file.exists() else "{}"
    try:
        state["forecasts"] = json.loads(cache_before)  # kept out of state.json: it is big and changes often
    except ValueError:
        state["forecasts"] = {}
    rng = random.Random(seed if seed is not None else int(now))
    problems: list[str] = []
    settled: list[dict] = []
    new: list[dict] = []
    sightings: list[dict] = []
    weather_notes: list[dict] = []
    weather_rows: list[dict] = []
    views: list[dict] = []
    timing: dict[str, float] = {}
    crash: BaseException | None = None

    def lap(name: str) -> None:
        timing[name] = round(time.time() - t0 - sum(timing.values()), 1)

    try:
        try:
            settled = settle(state, now, fetch)
        except pmapi.ApiError as e:
            problems.append(f"settle: {e}")
        lap("settle")
        stale = [p for p in state["positions"] if now - p.get("ends_at", now) > STALE_DAYS * 86400]
        if stale:
            problems.append(f"{len(stale)} position(s) still open more than {STALE_DAYS} days after their market ended")

        events: list[dict] = []
        try:
            events, more = list_events(now, fetch)
            problems += more
        except pmapi.ApiError as e:
            problems.append(f"events: {e}")
        views = [v for v in (market_view(m, now) for m in markets_of(events)) if v and v["hours_left"] > 0]
        events_by_id = {str(ev.get("id")): ev for ev in events}
        lap("list")

        # Temperature events for weather_forecast: the ones ending within the next few days.
        weather_on = S.STRATEGIES["weather_forecast"]["active"]
        horizon = now + weather.EVENT_DAYS * 86400
        temp_events = [ev for ev in events if weather.is_temperature_event(ev.get("title"))
                       and (parse_ts(ev.get("endDate")) or 0) <= horizon] if weather_on else []
        views_by_cid = {v["conditionId"]: v for v in views}

        picks = pick_entries(views, state, rng)
        lap("pick")
        if weather_on and temp_events:
            traded = _traded(state, "weather_forecast")
            # every temperature event gets its daily forecast snapshot (for checking the
            # forecasts later), held or not; only the buying skips events already held
            wf = weather.forecast_picks(temp_events, views_by_cid, state, now, fetch)
            problems += wf["problems"]
            weather_notes, weather_rows = wf["notes"], wf["rows"]
            wp = [p for p in wf["picks"] if p[0]["event_id"] not in traded]
            rng.shuffle(wp)
            picks["weather_forecast"] = wp[: S.MAX_NEW_PER_RUN]
        lap("weather")
        wanted = {v["tokens"][i] for c in picks.values() for v, i, _, _ in c}
        books: dict = {}
        try:
            books = pmapi.books(sorted(wanted), fetch) if wanted else {}
        except pmapi.ApiError as e:
            problems.append(f"books: {e}")
        for name, cands in picks.items():
            for v, i, cap, note in cands:
                t = make_trade(name, v, i, cap, books.get(v["tokens"][i]), now, note)
                if t:
                    new.append(t)
        lap("fill")

        if S.STRATEGIES["price_gap"]["active"]:
            try:
                gap, sightings = price_gap_trades(views, events_by_id, state, now, fetch)
                new.extend(gap)
            except pmapi.ApiError as e:
                problems.append(f"price_gap: {e}")
            lap("price_gap")
    except Exception as e:  # anything unexpected: record it, save what happened, then fail loudly
        crash = e
        problems.append(f"crash: {e!r}"[:300])

    for t in new:
        _traded(state, t["strategy"])
        state["traded_events"][t["strategy"]][t["event_id"]] = int(t["ends_at"] + REMEMBER_DAYS * 86400)
    for name, cur in state["traded_events"].items():
        for eid in [e for e, until in cur.items() if until < now]:
            del cur[eid]
    state["positions"].extend(new)
    for month in sorted({_month(t["opened_at"]) for t in new}):
        append_jsonl(data / "trades" / f"{month}.jsonl", [t for t in new if _month(t["opened_at"]) == month])
    for month in sorted({_month(s["settled_at"]) for s in settled}):
        append_jsonl(data / "settled" / f"{month}.jsonl", [s for s in settled if _month(s["settled_at"]) == month])
    day = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")
    append_jsonl(data / "gaps" / f"{day}.jsonl", sightings)
    append_jsonl(data / "weather" / f"{day}.jsonl", [dict(w, at=int(now)) for w in weather_notes])
    append_jsonl(data / "forecasts" / f"{day}.jsonl", [dict(w, at=int(now)) for w in weather_rows])

    run_row = {"at": int(now), "seconds": round(time.time() - t0, 1), "timing": timing, "markets": len(views),
               "new_trades": len(new), "settled": len(settled), "open": len(state["positions"]),
               "problems": problems}
    try:
        text, summary = report.build(data, now, state, run_row)
        write_text(data / "report.md", text)
        write_text(data / "summary.json", json.dumps(summary, indent=1, sort_keys=True))
    except Exception as e:  # the report must never cost the run its data
        problems.append(f"report: {e!r}"[:300])
        stamp = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        write_text(data / "report.md", "# Polymarket strategy lab\n\n"
                   f"The report could not be built at {stamp} UTC ({e!r}). The data is intact and the next run "
                   "will try again; see runs.jsonl.\n")
        if crash is None:
            crash = e
    run_row["seconds"] = round(time.time() - t0, 1)
    append_jsonl(data / "runs.jsonl", [run_row])  # last, so the row holds every problem, the report's included
    cache_after = json.dumps(state.pop("forecasts", {}), sort_keys=True)
    if cache_after != cache_before:
        write_text(cache_file, cache_after)
    write_text(data / "state.json", json.dumps(state, sort_keys=True))
    if crash is not None:
        raise crash
    return run_row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    args = ap.parse_args()
    row = run(args.data)
    print(json.dumps(row))


if __name__ == "__main__":
    main()
