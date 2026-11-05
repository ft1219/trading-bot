"""
Polymarket strategy lab: one run.

Pretend money only. Public data, no account, no keys, no orders.

Each run (every 40 minutes, inside the "Bots - every 40 minutes" workflow):
1. Settles pretend positions whose markets have resolved ($1 or $0 a share).
2. Lists every open market that ends within 7 days (Gamma).
3. Asks each strategy in strategies.py which markets it would buy.
4. Fills those buys against the real order book (walking the asks, up to
   the strategy's price cap) and adds Polymarket's taker fee.
5. Daily temperature markets: compares each range's price with the chance
   two weather-model ensembles give it, and buys where the price is at
   least 10 cents too low ("weather_forecast").
6. Looks for multi-choice markets whose prices add up to less than $1
   ("price_gap"), and fills those against the real books too.
7. Rewrites report.md / summary.json.

Data layout (the polymarket-lab-data branch):
- state.json: open positions and which events each strategy already traded
- trades.jsonl: every pretend buy, one per line
- settled.jsonl: every finished position with its result
- runs.jsonl: when each run happened, how long it took, and any problems
- gaps/YYYY-MM-DD.jsonl, weather/YYYY-MM-DD.jsonl: what price_gap and
  weather_forecast saw, trade or not
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
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
MAX_UNIVERSE = 6000
GAP_BUDGET_USD = 20.0  # most a price_gap trade may spend
GAP_MIN_EDGE = 0.005  # needs at least half a cent a share-set after fees
GAP_MAX_OUTCOMES = 40


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


def market_view(m: dict, now: float) -> dict | None:
    """Gamma market plus the fields strategies use; None if it cannot be traded."""
    end = parse_ts(m.get("endDate"))
    tokens = [str(t) for t in _json_list(m.get("clobTokenIds"))]
    if end is None or len(tokens) != 2 or not m.get("conditionId"):
        return None
    if m.get("closed") or not m.get("active") or m.get("acceptingOrders") is False or m.get("enableOrderBook") is False:
        return None
    v = dict(m)
    v["hours_left"] = (end - now) / 3600
    v["sport"] = m.get("sportsMarketType") or None
    start = parse_ts(m.get("gameStartTime"))
    v["hours_to_start"] = (start - now) / 3600 if start else None
    v["tokens"] = tokens
    v["outcomes"] = _json_list(m.get("outcomes"))
    ev = (m.get("events") or [{}])[0] or {}
    v["event_id"] = str(ev.get("id") or m["conditionId"])
    v["event_title"] = ev.get("title") or m.get("question")
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

def list_markets(now: float, fetch=pmapi.http_json) -> list[dict]:
    lo = dt.datetime.fromtimestamp(now, dt.timezone.utc)
    hi = lo + dt.timedelta(hours=HORIZON_HOURS)
    out: list[dict] = []
    # Gamma refuses offsets past about 2,000, so walk the week in 12-hour slices.
    a = lo
    while a < hi and len(out) < MAX_UNIVERSE:
        b = min(a + dt.timedelta(hours=12), hi)
        offset = 0
        while offset <= 2000:
            q = urllib.parse.urlencode({
                "active": "true", "closed": "false", "limit": 100, "offset": offset,
                "end_date_min": a.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end_date_max": b.strftime("%Y-%m-%dT%H:%M:%SZ")})
            page = fetch(f"{pmapi.GAMMA}/markets?{q}", None)
            if not isinstance(page, list):
                raise pmapi.ApiError("/markets: unexpected shape")
            out.extend(page)
            if len(page) < 100:
                break
            offset += 100
        a = b
    seen, uniq = set(), []
    for m in out:
        if m.get("conditionId") not in seen:
            seen.add(m.get("conditionId"))
            uniq.append(m)
    return uniq


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


def event_markets(event_id: str, fetch=pmapi.http_json) -> dict | None:
    rows = fetch(f"{pmapi.GAMMA}/events?id={urllib.parse.quote(event_id)}", None)
    return rows[0] if isinstance(rows, list) and rows else None


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

def _traded(state: dict, name: str) -> set:
    return set(state["traded_events"].setdefault(name, []))


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
                cands.append((v, hit[0], hit[1]))
                events.add(v["event_id"])
        rng.shuffle(cands)
        picks[name] = cands[: S.MAX_NEW_PER_RUN]
    return picks


def make_trade(name: str, v: dict, idx: int, cap: float, book: dict | None, now: float, note: dict | None = None) -> dict | None:
    shares, cost = fill_dollars(asks_of(book), S.STAKE_USD, cap, v["fee_rate"], v["fee_exp"])
    if cost < 1.0 or shares < 1:  # Polymarket's minimum order is about $1
        return None
    return {
        **({"note": note} if note else {}),
        "strategy": name, "opened_at": int(now), "event_id": v["event_id"],
        "title": (v.get("question") or "")[:140], "event": (v.get("event_title") or "")[:140],
        "sport": v["sport"], "hours_left": round(v["hours_left"], 2),
        "cost": round(cost, 6), "avg_price": round(cost / shares, 6),
        "legs": [{"condition_id": v["conditionId"], "outcome_index": idx,
                  "outcome": (v["outcomes"][idx] if idx < len(v["outcomes"]) else str(idx)),
                  "shares": round(shares, 6)}],
    }


def price_gap_trades(views: list[dict], state: dict, now: float, fetch=pmapi.http_json) -> tuple[list[dict], list[dict]]:
    """
    In a multi-choice ("neg-risk") event exactly one choice wins. If buying
    every Yes costs less than $1 a set, or every No less than (n-1) dollars,
    the difference is locked in. Returns (trades, sightings).
    """
    by_event: dict[str, list[dict]] = {}
    for v in views:
        if v.get("negRisk"):
            by_event.setdefault(v["event_id"], []).append(v)
    traded = _traded(state, "price_gap")
    trades, sightings = [], []
    for eid, ms in by_event.items():
        if eid in traded or len(ms) < 2 or len(ms) > GAP_MAX_OUTCOMES:
            continue
        try:
            asks = [float(m["bestAsk"]) for m in ms]
            bids = [float(m["bestBid"]) for m in ms]
        except (KeyError, TypeError, ValueError):
            continue
        yes_sum, no_sum = sum(asks), sum(1 - b for b in bids)
        if yes_sum >= 1.0 and no_sum >= len(ms) - 1:
            continue  # Gamma's quotes show no gap; skip the book calls
        try:
            ev = event_markets(eid, fetch)
        except pmapi.ApiError:
            continue
        legs_src = [market_view(m, now) for m in (ev or {}).get("markets") or []]
        if not ev or any(x is None for x in legs_src) or len(legs_src) != len(ms):
            continue  # a closed, paused or unlisted choice: not a complete set
        try:
            books = pmapi.books([t for x in legs_src for t in x["tokens"]], fetch)
        except pmapi.ApiError:
            continue
        for side, payout_per_set in ((0, 1.0), (1, float(len(legs_src) - 1))):
            books_side = [asks_of(books.get(x["tokens"][side])) for x in legs_src]
            best = None
            k = 1.0
            while True:
                costs = [fill_shares(b, k, x["fee_rate"], x["fee_exp"]) for b, x in zip(books_side, legs_src)]
                if any(c is None for c in costs):
                    break
                total = sum(costs)
                if total > GAP_BUDGET_USD or payout_per_set * k - total < GAP_MIN_EDGE * k:
                    break
                best = (k, total, costs)
                k += 1.0
            first = [fill_shares(b, 1.0, x["fee_rate"], x["fee_exp"]) for b, x in zip(books_side, legs_src)]
            if all(c is not None for c in first):
                sightings.append({"event_id": eid, "event": ev.get("title"), "side": "yes" if side == 0 else "no",
                                  "n": len(legs_src), "cost_per_set": round(sum(first), 4),
                                  "pays": payout_per_set, "at": int(now)})
            if best:
                k, total, costs = best
                trades.append({
                    "strategy": "price_gap", "opened_at": int(now), "event_id": eid,
                    "title": f"All {'Yes' if side == 0 else 'No'} on: {(ev.get('title') or '')[:110]}",
                    "event": (ev.get("title") or "")[:140], "sport": None, "hours_left": round(legs_src[0]["hours_left"], 2),
                    "cost": round(total, 6), "avg_price": round(total / k, 6),
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
    return st


def append_jsonl(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("a") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")


def run(data: Path, now: float | None = None, fetch=pmapi.http_json, seed: int | None = None) -> dict:
    now = time.time() if now is None else now
    t0 = time.time()
    data.mkdir(parents=True, exist_ok=True)
    state = load_state(data)
    rng = random.Random(seed if seed is not None else int(now))
    problems: list[str] = []

    settled: list[dict] = []
    try:
        settled = settle(state, now, fetch)
    except pmapi.ApiError as e:
        problems.append(f"settle: {e}")
    append_jsonl(data / "settled.jsonl", settled)

    raw: list[dict] = []
    try:
        raw = list_markets(now, fetch)
    except pmapi.ApiError as e:
        problems.append(f"markets: {e}")
    views = [v for v in (market_view(m, now) for m in raw) if v and v["hours_left"] > 0]

    # Temperature events, for weather_forecast. Their markets are usually in
    # the list already; any that are not are added so every strategy sees them.
    temp_events: list[dict] = []
    weather_on = S.STRATEGIES["weather_forecast"]["active"]
    if weather_on:
        try:
            temp_events = weather.list_events(now, fetch)
        except pmapi.ApiError as e:
            problems.append(f"weather events: {e}")
    known = {v["conditionId"] for v in views}
    for m in weather.as_markets(temp_events):
        v = market_view(m, now)
        if v and v["hours_left"] > 0 and v["conditionId"] not in known:
            views.append(v)
            known.add(v["conditionId"])
    views_by_cid = {v["conditionId"]: v for v in views}

    new: list[dict] = []
    picks = pick_entries(views, state, rng)
    notes: dict[str, dict] = {}
    weather_seen: list[dict] = []
    if weather_on and temp_events:
        traded = _traded(state, "weather_forecast")
        fresh = [e for e in temp_events if str(e.get("id")) not in traded]
        try:
            wp, weather_seen = weather.forecast_picks(fresh, views_by_cid, state, now, fetch)
        except pmapi.ApiError as e:
            wp = []
            problems.append(f"weather forecast: {e}")
        rng.shuffle(wp)
        picks["weather_forecast"] = [(v, i, cap) for v, i, cap, _ in wp[: S.MAX_NEW_PER_RUN]]
        for v, i, cap, prob in wp:
            notes[v["conditionId"]] = {"forecast_chance": round(prob, 3)}
    wanted = {v["tokens"][i] for c in picks.values() for v, i, _ in c}
    books: dict = {}
    try:
        books = pmapi.books(sorted(wanted), fetch) if wanted else {}
    except pmapi.ApiError as e:
        problems.append(f"books: {e}")
    for name, cands in picks.items():
        for v, i, cap in cands:
            t = make_trade(name, v, i, cap, books.get(v["tokens"][i]), now, notes.get(v["conditionId"]))
            if t:
                new.append(t)

    sightings: list[dict] = []
    if S.STRATEGIES["price_gap"]["active"]:
        try:
            gap, sightings = price_gap_trades(views, state, now, fetch)
            new.extend(gap)
        except pmapi.ApiError as e:
            problems.append(f"price_gap: {e}")

    for t in new:
        state["traded_events"].setdefault(t["strategy"], []).append(t["event_id"])
    state["positions"].extend(new)
    append_jsonl(data / "trades.jsonl", new)
    day = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")
    if sightings:
        (data / "gaps").mkdir(exist_ok=True)
        append_jsonl(data / "gaps" / f"{day}.jsonl", sightings)
    if weather_seen:
        (data / "weather").mkdir(exist_ok=True)
        append_jsonl(data / "weather" / f"{day}.jsonl", [dict(w, at=int(now)) for w in weather_seen])

    run_row = {"at": int(now), "seconds": round(time.time() - t0, 1), "markets": len(views),
               "new_trades": len(new), "settled": len(settled), "open": len(state["positions"]),
               "problems": problems}
    append_jsonl(data / "runs.jsonl", [run_row])
    (data / "state.json").write_text(json.dumps(state, sort_keys=True))
    text, summary = report.build(data, now)
    (data / "report.md").write_text(text)
    (data / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True))
    return run_row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    args = ap.parse_args()
    row = run(args.data)
    print(json.dumps(row))


if __name__ == "__main__":
    main()
