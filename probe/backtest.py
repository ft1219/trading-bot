"""
One-off, read-only backtest of the paper market maker over the last 7 days
of public data (trades and one-minute midpoints) for the 25 watched markets.
No book history exists, so it measures fills and trading results only, not
rewards, and values holdings at the midpoint. Compares the fill rule in use
(trades through our price + midpoint moves through it) with trades only.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import pmapi  # noqa: E402
import sim  # noqa: E402

DAYS = 7
LEVELS = (0, 1, 2)
pmapi.TRADES_MAX_PAGES = 80

_orig_events = sim._events


def _trades_only(records, times, start, end):
    return [e for e in _orig_events(records, times, start, end) if e[1] == 0]


VARIANTS = {"trades_and_mid_moves": _orig_events, "trades_only": _trades_only}


def mid_at(history, ts):
    best = None
    for t, m in history:
        if t <= ts:
            best = m
        else:
            break
    return best


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    markets = json.load(open(os.path.join(os.path.dirname(__file__), "markets_bt.json")))
    now = int(time.time()) // 3600 * 3600
    start = now - DAYS * 86400
    results = []
    for m in markets:
        cid, yes = m["condition_id"], m["yes_token"]
        entry = {k: m.get(k) for k in ("rank", "pilot", "thin", "question", "daily_rate", "expected_low",
                                        "expected_high", "mid", "tick", "max_spread_c", "min_size", "fee_rate", "rebate_rate")}
        entry["condition_id"] = cid
        try:
            hist = []
            for d in range(DAYS):
                a = start + d * 86400
                hist += pmapi.price_history(yes, a, a + 86400)
            hist = sorted(set(hist))
            trades, complete = pmapi.trades_since(cid, start)
        except Exception as e:
            entry["error"] = repr(e)
            results.append(entry)
            continue
        entry.update(history_points=len(hist), trades=len(trades), trades_complete=complete,
                     first_hist=hist[0][0] if hist else None)
        p = sim.MarketParams(tick=float(m["tick"]), size=float(m["size"]), budget_usd=20.0,
                             max_spread_c=float(m["max_spread_c"]), fee_rate=float(m.get("fee_rate") or 0),
                             fee_exponent=float(m.get("fee_exponent") or 1), rebate_rate=float(m.get("rebate_rate") or 0))
        entry["runs"] = {}
        for vname, events in VARIANTS.items():
            sim._events = events
            for level in LEVELS:
                pos = sim.Position()
                days = []
                for d in range(DAYS):
                    a, b = start + d * 86400, start + (d + 1) * 86400
                    recs = [t for t in trades if a < int(t["timestamp"]) <= b]
                    stats = {}
                    fills = sim.replay(pos, recs, hist, yes, p, level, start=a, end=b, stats=stats)
                    mid_end = mid_at(hist, b)
                    days.append({"day": d, "fills": len(fills),
                                 "mid_fills": sum(1 for f in fills if f.tx == "midpoint-move"),
                                 "shares": round(sum(f.shares for f in fills), 2),
                                 "value_mid": None if mid_end is None else round(pos.value(mid_end), 4),
                                 "rebates": round(pos.rebates, 4), "yes": round(pos.yes, 2), "no": round(pos.no, 2),
                                 "mid_end": mid_end, "unquoted": stats.get("unquoted_trades", 0)})
                entry["runs"][f"{vname}/L{level}"] = days
            sim._events = _orig_events
        results.append(entry)
        time.sleep(0.2)
    json.dump({"start": start, "end": now, "days": DAYS, "markets": results},
              open(os.path.join(out_dir, "backtest_7d.json"), "w"), indent=1)

    print(f"window {start}..{now} ({DAYS} days); trading result valued at the midpoint, per day")
    for e in results:
        if "error" in e:
            print(e["rank"], "ERROR", e["error"])
            continue
        line = [f"r{e['rank']:>2}", "PILOT" if e["pilot"] else ("thin " if e["thin"] else "     "),
                f"trades={e['trades']:>5}{'' if e['trades_complete'] else '+'}", f"pts={e['history_points']:>5}",
                f"rew_est={e['expected_low'] or 0:6.2f}-{e['expected_high'] or 0:6.2f}"]
        for key in ("trades_and_mid_moves/L1", "trades_only/L1", "trades_and_mid_moves/L0", "trades_only/L0"):
            days = e["runs"][key]
            last = days[-1]
            v = last["value_mid"] if last["value_mid"] is not None else float("nan")
            line.append(f"{key.replace('trades_and_mid_moves', 'all').replace('trades_only', 'tr')}: "
                        f"{v / DAYS:+6.2f}/d f={sum(x['fills'] for x in days):>3}(m{sum(x['mid_fills'] for x in days)}) "
                        f"reb={last['rebates']:.2f}")
        print("  ".join(line))
    print("question per rank:")
    for e in results:
        print(e["rank"], (e.get("question") or "")[:70])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
