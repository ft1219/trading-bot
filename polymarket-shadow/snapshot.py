"""
One practice-mode run: no money, no account, public data only.

Each run (every 40 minutes, inside the scheduled GitHub Actions job):
1. Once a UTC day, picks the watchlist from all liquidity-reward markets.
2. For each watched market, replays the public trades and midpoint moves
   since the last run against our paper quotes (see sim.py) at three
   distances from the midpoint, and records any fills.
3. Reads the live order book and records what share of the market's daily
   reward pool our paper orders would be earning now (see rewards.py). In a
   thin market the cautious estimate counts no reward at all.
4. Values each paper position at what it would sell for now, and an hour
   and a day after each fill records how far the price moved (markouts).
5. Rewrites the report.

Everything is stored as plain files in the data folder (the
polymarket-shadow-data branch in Actions).

Usage: python snapshot.py --data DIR [--now UNIX_SECONDS]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import pmapi
import report
import rewards
import selection
import sim

LEVELS = (0, 1, 2)
MARKOUT_HORIZONS_S = (3600, 86400)
TRADE_SETTLE_S = 120  # data-api can list a trade a little late; leave a margin
FIRST_SAMPLE_DT_S = 2400
MAX_SAMPLE_DT_S = 3600
STATE_VERSION = 1


def settings_from_env(env=os.environ) -> selection.Settings:
    def num(name, default, kind=float):
        raw = (env.get(name) or "").strip()
        return kind(raw) if raw else default
    d = selection.Settings()
    return selection.Settings(
        budget_per_market_usd=num("PM_BUDGET_PER_MARKET_USD", d.budget_per_market_usd),
        watch_markets=num("PM_WATCH_MARKETS", d.watch_markets, int),
        pilot_markets=num("PM_PILOT_MARKETS", d.pilot_markets, int),
        thin_markets=num("PM_THIN_MARKETS", d.thin_markets, int),
        pilot_level=num("PM_PILOT_LEVEL", d.pilot_level, int),
        min_daily_rate_usd=num("PM_MIN_DAILY_RATE_USD", d.min_daily_rate_usd),
        min_days_to_end=num("PM_MIN_DAYS_TO_END", d.min_days_to_end),
    )


def utc_day(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d")


class Store:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)

    def load_state(self) -> dict:
        path = self.root / "state.json"
        if path.exists():
            return json.loads(path.read_text())
        return {"version": STATE_VERSION, "watchlist_day": None, "markets": {}, "pending_markouts": []}

    def save_state(self, state: dict) -> None:
        tmp = self.root / "state.json.tmp"
        tmp.write_text(json.dumps(state, indent=1, sort_keys=True))
        tmp.replace(self.root / "state.json")

    def append(self, day: str, name: str, rows: list[dict]) -> None:
        if not rows:
            return
        folder = self.root / "days" / day
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / f"{name}.jsonl", "a", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, sort_keys=True) + "\n")

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def params_for(info: dict, s: selection.Settings) -> sim.MarketParams:
    return sim.MarketParams(
        tick=float(info["tick"]), size=float(info["size"]), budget_usd=s.budget_per_market_usd,
        max_spread_c=float(info["max_spread_c"]), fee_rate=float(info.get("fee_rate") or 0),
        fee_exponent=float(info.get("fee_exponent") or 1), rebate_rate=float(info.get("rebate_rate") or 0),
    )


def refresh_watchlist(state: dict, store: Store, s: selection.Settings, now: float, api=pmapi) -> tuple[dict, set[str]]:
    """Pick today's markets; close out paper positions in markets that dropped off."""
    today = utc_day(now)
    sampling = api.sampling_markets()
    configs = api.current_reward_configs()
    cands = selection.prefilter(sampling, configs, dt.datetime.fromtimestamp(now, dt.timezone.utc), s)
    top = cands[: s.books_to_check]
    books = api.books([c.yes_token for c in top])
    scored = selection.score_candidates(top, books, s)
    chosen = selection.choose(scored, s)
    gamma = api.gamma_markets([c.condition_id for c in chosen])
    for c in chosen:
        selection.apply_fees(c, gamma.get(c.condition_id))

    chosen_ids = {c.condition_id for c in chosen}
    # Markets leaving the list are sold off by run() after their last trades are replayed.
    dropped = [cid for cid in state["markets"] if cid not in chosen_ids]
    for cid in dropped:
        state["markets"][cid]["closing"] = True
    for c in chosen:
        info = c.to_dict()
        m = state["markets"].get(c.condition_id)
        if m is not None:
            m.pop("closing", None)
            if bool(m["info"].get("pilot")) != c.pilot and "close_role" not in m:
                # Entering or leaving the pilot: sell off and restart the paper position, so the
                # pilot's result has only what it did while it was the pilot.
                m["close_role"] = bool(m["info"].get("pilot"))
            m["info"].update(
                {k: info[k] for k in ("pilot", "rank", "daily_rate", "max_spread_c", "min_size", "expected_low",
                                      "expected_high", "thin", "fee_rate", "fee_exponent", "rebate_rate",
                                      "end_date")})
        else:
            state["markets"][c.condition_id] = {
                "info": info, "added_ts": int(now),
                "trades_until": int(now) - TRADE_SETTLE_S, "last_sample_ts": None,
                "positions": {str(level): sim.Position().to_dict() for level in LEVELS},
            }
    state["watchlist_day"] = today
    store.append(today, "watchlist", [dict(c.to_dict(), ts=int(now)) for c in chosen])
    stats = {"candidates": len(cands), "scored": len(scored), "chosen": len(chosen), "dropped": len(dropped)}
    return stats, chosen_ids


def mid_at(history: list[tuple[int, float]], target: int, tolerance: int = 900) -> float | None:
    """First midpoint at or after target (or the last one shortly before)."""
    after = [p for t, p in history if target <= t <= target + tolerance]
    if after:
        return after[0]
    before = [p for t, p in history if target - tolerance <= t < target]
    return before[-1] if before else None


def _process_market(cid: str, m: dict, trades_result: tuple[list[dict], bool], history: list[tuple[int, float]],
                    books: dict, state: dict, out: dict, log: dict, s: selection.Settings, now: float,
                    just_chosen: bool) -> bool:
    """Replay, close out or sample one market. Returns True when the market has left the list."""
    info = m["info"]
    trades, complete = trades_result
    cutoff = int(now) - TRADE_SETTLE_S
    since = int(m["trades_until"])
    gap_reasons = []
    if not complete:
        gap_reasons.append("trade history cut short")
    trades = [t for t in trades if int(t["timestamp"]) <= cutoff]
    p = params_for(info, s)
    stats = {"unquoted_trades": 0}
    positions, fills = {}, []
    for level in LEVELS:  # replay on copies; nothing is stored unless every level succeeds
        pos = sim.Position.from_dict(m["positions"][str(level)])
        for f in sim.replay(pos, trades, history, info["yes_token"], p, level, start=since, end=cutoff, stats=stats):
            fills.append({"condition_id": cid, "pilot": info.get("pilot", False), "rank": info.get("rank"),
                          "ts": f.ts, "level": level, "side": f.side, "price": f.price, "shares": f.shares,
                          "mid_before": f.mid_before, "trade_price": f.trade_price, "rebate": round(f.rebate, 6),
                          "tx": f.tx})
        positions[str(level)] = pos.to_dict()
    if stats["unquoted_trades"]:
        gap_reasons.append(f"{stats['unquoted_trades']} trade(s) with no recent midpoint")
    if cutoff - since > sim.MAX_QUOTE_AGE_S and not any(since < t <= cutoff for t, _ in history):
        gap_reasons.append("no midpoint history for the window")
    m["positions"] = positions
    m["trades_until"] = max(since, cutoff)
    out["fills"].extend(fills)
    for row in fills:
        for h in MARKOUT_HORIZONS_S:
            state["pending_markouts"].append(dict(row, horizon=h, target=row["ts"] + h, yes_token=info["yes_token"]))
    if gap_reasons:  # some of this window was not replayed: the day does not count for this market
        log["errors"].append(f"{cid[:10]}: " + "; ".join(gap_reasons))
        out["gaps"].append({"ts": int(now), "condition_id": cid, "pilot": info.get("pilot", False),
                            "reason": "; ".join(gap_reasons)})

    raw = books.get(info["yes_token"])
    book = rewards.parse_book(raw) if raw else None
    if m.get("closing") or "close_role" in m:
        if book is None:
            log["errors"].append(f"{cid[:10]}: no book to close out with, trying next run")
            return False
        role = m.get("close_role", info.get("pilot", False))
        rows = []
        for level, pd in m["positions"].items():
            pos = sim.Position.from_dict(pd)
            received = sim.close_out(pos, book, p)  # shares nobody would buy are left behind, worth nothing
            rows.append({
                "ts": int(now), "condition_id": cid, "level": int(level), "pilot": role,
                "value_after": round(pos.cash, 6), "received": round(received, 6),
                "unsold_yes": pos.yes, "unsold_no": pos.no, "rebates": round(pos.rebates, 6),
            })
        out["closeouts"].extend(rows)
        m.pop("close_role", None)
        if m.get("closing"):
            return True
        m["positions"] = {str(level): sim.Position().to_dict() for level in LEVELS}
        m["last_sample_ts"] = int(now)
        return False

    if just_chosen:
        # This run's books picked the watchlist; scoring them too would credit the
        # pilots with the moment they looked best. The next run takes the first sample.
        m["last_sample_ts"] = int(now)
        return False
    if book is None:
        log["errors"].append(f"{cid[:10]}: no book")
        return False
    mid = rewards.raw_midpoint(book)  # the same midpoint the paper fills are quoted from
    if mid is None:
        log["errors"].append(f"{cid[:10]}: no usable midpoint")
        return False
    last = m.get("last_sample_ts")
    dt_s = FIRST_SAMPLE_DT_S if last is None else min(int(now) - int(last), MAX_SAMPLE_DT_S)
    v, min_size = float(info["max_spread_c"]), float(info["min_size"])
    row = {"ts": int(now), "condition_id": cid, "pilot": info.get("pilot", False), "rank": info.get("rank"),
           "rate": info["daily_rate"], "mid": mid, "dt": dt_s, "levels": {}}
    for level in LEVELS:
        pos = sim.Position.from_dict(m["positions"][str(level)])
        bid, ask = sim.quotes(mid, p, level)
        bid_on, ask_on = sim.active_sides(pos, bid, ask, p)
        sc = rewards.score_quotes(book, bid if bid_on else None, ask if ask_on else None, p.size, v, min_size)
        share_low = 0.0 if sc.thin else sc.ours.share_low
        row["levels"][str(level)] = {
            "bid": bid if bid_on else None, "ask": ask if ask_on else None, "reward_mid": sc.reward_mid,
            "thin": sc.thin, "q": round(sc.ours.q_min, 4), "comp_low": round(sc.comp.low, 3),
            "comp_high": round(sc.comp.high, 3), "share_low": share_low, "share_high": sc.ours.share_high,
            "est_low": info["daily_rate"] * share_low * dt_s / 86400,
            "est_high": info["daily_rate"] * sc.ours.share_high * dt_s / 86400,
            "value": round(sim.liquidation_value(pos, book, p), 6),
            "value_mid": round(pos.value(mid), 6), "rebates": round(pos.rebates, 6), "fills": pos.fills,
            "yes": pos.yes, "no": pos.no,
        }
    row["thin"] = row["levels"].get(str(s.pilot_level), row["levels"]["1"])["thin"]
    out["samples"].append(row)
    m["last_sample_ts"] = int(now)
    return False


def run(data_dir: Path, now: float | None = None, api=pmapi, s: selection.Settings | None = None) -> dict:
    started = time.time()
    now = float(now if now is not None else time.time())
    s = s or settings_from_env()
    store = Store(data_dir)
    state = store.load_state()
    today = utc_day(now)
    log: dict = {"ts": int(now), "errors": []}

    just_chosen: set[str] = set()
    if state.get("watchlist_day") != today or not state["markets"]:
        try:
            log["refresh"], just_chosen = refresh_watchlist(state, store, s, now, api)
        except Exception as e:  # keep going with yesterday's list
            log["errors"].append(f"refresh: {e!r}")

    markets = state["markets"]
    calls = {}
    for cid, m in markets.items():
        info, since = m["info"], int(m["trades_until"])
        calls[f"trades:{cid}"] = (lambda cid=cid, since=since: api.trades_since(cid, since))
        calls[f"hist:{cid}"] = (lambda tok=info["yes_token"], since=since: api.price_history(tok, since - 900, int(now)))
    calls["books"] = lambda: api.books([m["info"]["yes_token"] for m in markets.values()])
    fetched = api.parallel(calls) if markets else {}
    books = fetched.get("books")
    if isinstance(books, Exception):
        log["errors"].append(f"books: {books!r}")
        books = {}

    out = {"fills": [], "samples": [], "gaps": [], "closeouts": []}
    histories: dict[str, list[tuple[int, float]]] = {}
    finished: list[str] = []
    for cid, m in markets.items():
        trades = fetched.get(f"trades:{cid}")
        history = fetched.get(f"hist:{cid}")
        if isinstance(trades, Exception) or isinstance(history, Exception):
            log["errors"].append(f"{cid[:10]}: {trades if isinstance(trades, Exception) else history!r}")
            continue  # timestamps stay put, so the next run covers this window
        histories[cid] = history
        try:
            if _process_market(cid, m, trades, history, books, state, out, log, s, now, cid in just_chosen):
                finished.append(cid)
        except Exception as e:  # one market's bad data must not stop the others
            log["errors"].append(f"{cid[:10]}: {e!r}")
    for cid in finished:
        markets.pop(cid)
    fills_out, samples_out, gaps_out = out["fills"], out["samples"], out["gaps"]
    markouts_out: list[dict] = []

    # Markouts: an hour and a day after each paper fill.
    still_pending = []
    need_history = {}
    for item in state["pending_markouts"]:
        if item["target"] > now - 60:
            still_pending.append(item)
            continue
        hist = histories.get(item["condition_id"])
        later = mid_at(hist, item["target"]) if hist else None
        if later is None:
            need_history.setdefault(item["yes_token"], []).append(item)
            continue
        markouts_out.append(_markout_row(item, later))
    if need_history:
        extra = api.parallel({tok: (lambda tok=tok, items=items: api.price_history(
            tok, min(i["target"] for i in items) - 900, max(i["target"] for i in items) + 900))
            for tok, items in need_history.items()})
        for tok, items in need_history.items():
            hist = extra.get(tok)
            for item in items:
                later = mid_at(hist, item["target"]) if isinstance(hist, list) else None
                if later is not None:
                    markouts_out.append(_markout_row(item, later))
                elif now - item["target"] < 3 * 86400:
                    still_pending.append(item)  # try again next run
    state["pending_markouts"] = still_pending

    store.append(today, "closeouts", out["closeouts"])
    store.append(today, "fills", fills_out)
    store.append(today, "samples", samples_out)
    store.append(today, "markouts", markouts_out)
    store.append(today, "gaps", gaps_out)
    log.update({"markets": len(markets), "samples": len(samples_out), "fills": len(fills_out),
                "markouts": len(markouts_out), "seconds": round(time.time() - started, 2)})
    store.append(today, "runs", [log])
    state["version"] = STATE_VERSION
    store.save_state(state)
    try:
        text, summary = report.build(data_dir, s, now)
        store.write("report.md", text)
        store.write("summary.json", json.dumps(summary, indent=1, sort_keys=True))
    except Exception as e:
        log["errors"].append(f"report: {e!r}")
    return log


def _markout_row(item: dict, later_mid: float) -> dict:
    return {
        "condition_id": item["condition_id"], "pilot": item.get("pilot", False), "level": item["level"],
        "fill_ts": item["ts"], "horizon": item["horizon"], "side": item["side"], "price": item["price"],
        "shares": item["shares"], "later_mid": later_mid,
        "markout_usd": round(sim.markout(item["side"], item["price"], later_mid, item["shares"]), 6),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--data", required=True)
    parser.add_argument("--now", type=float, default=None)
    args = parser.parse_args(argv)
    log = run(Path(args.data), args.now)
    print(json.dumps(log, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
