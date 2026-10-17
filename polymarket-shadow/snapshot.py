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


def refresh_watchlist(state: dict, store: Store, s: selection.Settings, now: float, api=pmapi) -> dict:
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
    dropped = [cid for cid in state["markets"] if cid not in chosen_ids]
    closeouts: list[dict] = []
    if dropped:
        drop_books = api.books([state["markets"][cid]["info"]["yes_token"] for cid in dropped])
        for cid in dropped:
            m = state["markets"].pop(cid)
            raw = drop_books.get(m["info"]["yes_token"])
            book = rewards.parse_book(raw) if raw else None
            for level, pd in m["positions"].items():
                pos = sim.Position.from_dict(pd)
                before = pos.cash
                sim.close_out(pos, book.best_bid if book else None, book.best_ask if book else None)
                closeouts.append({
                    "ts": int(now), "condition_id": cid, "level": int(level), "pilot": m["info"].get("pilot", False),
                    "value_after": round(pos.cash, 6), "received": round(pos.cash - before, 6),
                    "unsold_yes": pos.yes, "unsold_no": pos.no, "rebates": round(pos.rebates, 6),
                })
    for c in chosen:
        info = c.to_dict()
        if c.condition_id in state["markets"]:
            state["markets"][c.condition_id]["info"].update(
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
    store.append(today, "closeouts", closeouts)
    return {"candidates": len(cands), "scored": len(scored), "chosen": len(chosen), "dropped": len(dropped)}


def mid_at(history: list[tuple[int, float]], target: int, tolerance: int = 900) -> float | None:
    """First midpoint at or after target (or the last one shortly before)."""
    after = [p for t, p in history if target <= t <= target + tolerance]
    if after:
        return after[0]
    before = [p for t, p in history if target - tolerance <= t < target]
    return before[-1] if before else None


def run(data_dir: Path, now: float | None = None, api=pmapi, s: selection.Settings | None = None) -> dict:
    started = time.time()
    now = float(now if now is not None else time.time())
    s = s or settings_from_env()
    store = Store(data_dir)
    state = store.load_state()
    today = utc_day(now)
    log: dict = {"ts": int(now), "errors": []}

    if state.get("watchlist_day") != today or not state["markets"]:
        try:
            log["refresh"] = refresh_watchlist(state, store, s, now, api)
        except Exception as e:  # keep going with yesterday's list
            log["errors"].append(f"refresh: {e!r}")

    markets = state["markets"]
    cutoff = int(now) - TRADE_SETTLE_S
    calls = {}
    for cid, m in markets.items():
        info, since = m["info"], int(m["trades_until"])
        calls[f"trades:{cid}"] = (lambda cid=cid, since=since: api.taker_trades_since(cid, since))
        calls[f"hist:{cid}"] = (lambda tok=info["yes_token"], since=since: api.price_history(tok, since - 900, int(now)))
    calls["books"] = lambda: api.books([m["info"]["yes_token"] for m in markets.values()])
    fetched = api.parallel(calls) if markets else {}
    books = fetched.get("books")
    if isinstance(books, Exception):
        log["errors"].append(f"books: {books!r}")
        books = {}

    fills_out, samples_out, markouts_out = [], [], []
    histories: dict[str, list[tuple[int, float]]] = {}
    for cid, m in markets.items():
        info = m["info"]
        trades = fetched.get(f"trades:{cid}")
        history = fetched.get(f"hist:{cid}")
        if isinstance(trades, Exception) or isinstance(history, Exception):
            log["errors"].append(f"{cid[:10]}: {trades if isinstance(trades, Exception) else history!r}")
            continue  # timestamps stay put, so the next run covers this window
        trades, complete = trades
        if not complete:
            log["errors"].append(f"{cid[:10]}: trade history cut short")
        histories[cid] = history
        trades = [t for t in trades if int(t["timestamp"]) <= cutoff]
        p = params_for(info, s)
        since = int(m["trades_until"])
        for level in LEVELS:
            pos = sim.Position.from_dict(m["positions"][str(level)])
            for f in sim.replay(pos, trades, history, info["yes_token"], p, level, start=since, end=cutoff):
                row = {"condition_id": cid, "pilot": info.get("pilot", False), "rank": info.get("rank"),
                       "ts": f.ts, "level": level, "side": f.side, "price": f.price, "shares": f.shares,
                       "mid_before": f.mid_before, "trade_price": f.trade_price, "rebate": round(f.rebate, 6),
                       "tx": f.tx}
                fills_out.append(row)
                for h in MARKOUT_HORIZONS_S:
                    state["pending_markouts"].append(dict(row, horizon=h, target=f.ts + h, yes_token=info["yes_token"]))
            m["positions"][str(level)] = pos.to_dict()
        m["trades_until"] = max(int(m["trades_until"]), cutoff)

        raw = books.get(info["yes_token"])
        if not raw:
            log["errors"].append(f"{cid[:10]}: no book")
            continue
        book = rewards.parse_book(raw)
        mid = rewards.adjusted_midpoint(book, float(info["min_size"]))
        if mid is None:
            log["errors"].append(f"{cid[:10]}: no usable midpoint")
            continue
        last = m.get("last_sample_ts")
        dt_s = FIRST_SAMPLE_DT_S if last is None else min(int(now) - int(last), MAX_SAMPLE_DT_S)
        v, min_size = float(info["max_spread_c"]), float(info["min_size"])
        thin = rewards.is_thin(book, mid, v, min_size)
        comp = rewards.competition(book, mid, v, min_size)
        row = {"ts": int(now), "condition_id": cid, "pilot": info.get("pilot", False), "rank": info.get("rank"),
               "rate": info["daily_rate"], "mid": round(mid, 5), "thin": thin, "comp_low": round(comp.low, 3),
               "comp_high": round(comp.high, 3), "dt": dt_s, "levels": {}}
        for level in LEVELS:
            pos = sim.Position.from_dict(m["positions"][str(level)])
            bid, ask = sim.quotes(mid, p, level)
            bid_on, ask_on = sim.active_sides(pos, bid, ask, p, now)
            matched = rewards.competition(book, mid, v, min_size,
                                          bid_c=(mid - bid) * 100 if bid is not None else None,
                                          ask_c=(ask - mid) * 100 if ask is not None else None)
            ours = rewards.our_score(bid if bid_on else None, ask if ask_on else None, p.size, mid,
                                     v, min_size, matched)
            share_low = 0.0 if thin else ours.share_low
            row["levels"][str(level)] = {
                "bid": bid if bid_on else None, "ask": ask if ask_on else None,
                "q": round(ours.q_min, 4), "comp_high": round(matched.high, 3),
                "share_low": share_low, "share_high": ours.share_high,
                "est_low": info["daily_rate"] * share_low * dt_s / 86400,
                "est_high": info["daily_rate"] * ours.share_high * dt_s / 86400,
                "value": round(pos.liquidation_value(book.best_bid, book.best_ask), 6),
                "value_mid": round(pos.value(mid), 6), "rebates": round(pos.rebates, 6), "fills": pos.fills,
                "yes": pos.yes, "no": pos.no,
            }
        samples_out.append(row)
        m["last_sample_ts"] = int(now)

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

    store.append(today, "fills", fills_out)
    store.append(today, "samples", samples_out)
    store.append(today, "markouts", markouts_out)
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
