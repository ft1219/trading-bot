"""
Turns the recorded practice data into a daily table and the go/no-go check.

Gate A (fixed before any data, in the project plan): go live with a small
pilot (2 markets, $20 each, orders 1 tick behind the closest prices) only
if, over at least 14 well-covered days, the cautious estimate for the pilot
markets of
    liquidity rewards + maker rebates + paper trading result
averages more than $1.50 a day.

"Cautious" means: competitors are assumed as strong as the order book allows
(and to move up to our price), a thin market earns nothing, time without a
sample (or without a usable book) earns nothing, holdings are valued at what
they would sell for, and the $1 minimum payout is applied to each market
separately (it may in fact apply to the whole account, which is the
"optimistic" column).

Rewards and rebates are averaged over the well-covered days only, but the
paper trading result is averaged over every day since the first pilot, so
losses on a badly covered day still count.

The "trades only" figures replay the same quotes with fills from trades
alone (no fills when only the midpoint moves through our price). They are
shown for comparison: the truth is likely between the two, and the check
uses the stricter one.
"""
from __future__ import annotations

import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

GATE_A_USD_PER_DAY = 1.50
GATE_A_MIN_DAYS = 14
PLAN = {"pilot_markets": 2, "budget_per_market_usd": 20.0, "pilot_level": 1}  # what the $1.50 bar was set for
MIN_COVERAGE = 0.5
MIN_PAYOUT_USD = 1.0
REPORT_DAYS = 35


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # a cut-off line from an interrupted run
    return rows


def _floor(x: float) -> float:
    return x if x >= MIN_PAYOUT_USD else 0.0


def _final_pilots(watchlist: list[dict]) -> set[str] | None:
    """The pilot markets of the day's last successful watchlist refresh (None: no refresh that day)."""
    if not watchlist:
        return None
    last = max(r["ts"] for r in watchlist)
    return {r["condition_id"] for r in watchlist if r["ts"] == last and r.get("pilot")}


def daily_rows(data_dir: Path, pilot_level: int, now: float) -> list[dict]:
    """
    One row per UTC day since the first. Values and rebates in the data are
    running totals per market, so every day is read to take differences. Each
    sample and closeout counts towards the
    pilot or not according to its own flag, because a market's role can change
    during a day (its paper position is closed out and restarted when it does).
    """
    days_dir = data_dir / "days"
    if not days_dir.exists():
        return []
    day_names = sorted(p.name for p in days_dir.iterdir() if p.is_dir())
    last_value: dict[tuple[str, int], float] = {}
    last_alt: dict[tuple[str, int], float] = {}  # the trades-only replay
    last_rebates: dict[tuple[str, int], float] = {}
    out = []
    for day in day_names:
        folder = days_dir / day
        samples = _read_jsonl(folder / "samples.jsonl")
        closeouts = _read_jsonl(folder / "closeouts.jsonl")
        fills = _read_jsonl(folder / "fills.jsonl")
        markouts = _read_jsonl(folder / "markouts.jsonl")
        gaps = _read_jsonl(folder / "gaps.jsonl")
        gap_ids = {g["condition_id"] for g in gaps}
        final_pilots = _final_pilots(_read_jsonl(folder / "watchlist.jsonl"))
        # Every run records its pilot settings; a day run under others cannot be judged against the bar.
        plan_ok = all(r.get("plan", PLAN) == PLAN for r in _read_jsonl(folder / "runs.jsonl"))

        # (condition_id, level, counted as pilot) -> the day's totals
        per: dict[tuple[str, int, bool], dict] = defaultdict(
            lambda: {"low": 0.0, "high": 0.0, "dt": 0, "thin_dt": 0, "rebates": 0.0, "trading": 0.0,
                     "trading_alt": 0.0, "closeout_thin": False})
        events = [(c["ts"], 0, c) for c in closeouts] + [(r["ts"], 1, r) for r in samples]
        for _, kind, row in sorted(events, key=lambda e: (e[0], e[1])):
            role = bool(row.get("pilot", False))
            if kind == 0:  # a paper position sold off when the market left the list or changed role
                key = (row["condition_id"], int(row["level"]))
                agg = per[key + (role,)]
                agg["trading"] += row["value_after"] - last_value.get(key, 0.0)
                agg["rebates"] += row.get("rebates", 0.0) - last_rebates.get(key, 0.0)
                agg["closeout_thin"] = bool(row.get("thin"))
                if row.get("value_after_trades_only") is not None:
                    agg["trading_alt"] += row["value_after_trades_only"] - last_alt.get(key, 0.0)
                last_value[key] = last_rebates[key] = last_alt[key] = 0.0
                continue
            for lv, d in row["levels"].items():
                key = (row["condition_id"], int(lv))
                agg = per[key + (role,)]
                agg["low"] += d["est_low"]
                agg["high"] += d["est_high"]
                agg["dt"] += row["dt"]
                agg["thin_dt"] += row["dt"] if row.get("thin") else 0
                agg["rebates"] += d["rebates"] - last_rebates.get(key, 0.0)
                last_rebates[key] = d["rebates"]
                if d.get("value") is not None:  # None: no book to value the holdings against this run
                    agg["trading"] += d["value"] - last_value.get(key, 0.0)
                    last_value[key] = d["value"]
                if d.get("value_trades_only") is not None:
                    agg["trading_alt"] += d["value_trades_only"] - last_alt.get(key, 0.0)
                    last_alt[key] = d["value_trades_only"]

        result = {"day": day, "plan_ok": plan_ok, "levels": {}}
        for level in sorted({k[1] for k in per} | {pilot_level}):
            mk = []
            for (cid, lv, role), agg in per.items():
                if lv != level:
                    continue
                coverage = agg["dt"] / 86400  # time not covered by a sample earns nothing (no scaling up)
                # thin for most of the day, or (only closed out today) when it left the list
                thin = not role and (agg["thin_dt"] * 2 > agg["dt"] if agg["dt"] else agg["closeout_thin"])
                mk.append({"condition_id": cid, "pilot": role, "thin": thin, "coverage": coverage,
                           "rewards_low": agg["low"], "rewards_high": agg["high"],
                           "rebates": agg["rebates"], "trading": agg["trading"], "trading_alt": agg["trading_alt"]})
            pilot = [x for x in mk if x["pilot"]]
            est = [x for x in mk if not x["thin"]]
            thin_mk = [x for x in mk if x["thin"]]
            if final_pilots is None:
                final_pilots_lv = {x["condition_id"] for x in pilot}
            else:
                final_pilots_lv = final_pilots
            coverage_of = {x["condition_id"]: x["coverage"] for x in pilot}
            covered = (bool(final_pilots_lv)
                       and all(coverage_of.get(cid, 0.0) >= MIN_COVERAGE for cid in final_pilots_lv)
                       and not (gap_ids & {x["condition_id"] for x in pilot})  # some trades were never replayed
                       and not any(g.get("pilot") for g in gaps))
            result["levels"][str(level)] = {
                "markets": len({x["condition_id"] for x in mk}),
                "pilot_markets": len({x["condition_id"] for x in pilot}),
                "pilot_covered": covered,
                "pilot_income": sum(_floor(x["rewards_low"]) + _floor(x["rebates"]) for x in pilot),
                "pilot_cautious": sum(_floor(x["rewards_low"]) + _floor(x["rebates"]) + x["trading"] for x in pilot),
                "pilot_optimistic": _floor(sum(x["rewards_high"] for x in pilot)) + _floor(sum(x["rebates"] for x in pilot))
                + sum(x["trading"] for x in pilot),
                "pilot_rewards_low": sum(x["rewards_low"] for x in pilot),
                "pilot_trading": sum(x["trading"] for x in pilot),
                "pilot_trading_trades_only": sum(x["trading_alt"] for x in pilot),
                "all_markets": len({x["condition_id"] for x in est}),
                "all_rewards_low": sum(x["rewards_low"] for x in est),
                "all_rewards_high": sum(x["rewards_high"] for x in est),
                "all_rebates": sum(x["rebates"] for x in est),
                "all_trading": sum(x["trading"] for x in est),
                "all_trading_trades_only": sum(x["trading_alt"] for x in est),
                "thin_markets": len({x["condition_id"] for x in thin_mk}),
                "thin_rewards_high": sum(x["rewards_high"] for x in thin_mk),
                "thin_trading": sum(x["trading"] for x in thin_mk),
                "fills": sum(1 for f in fills if int(f["level"]) == level),
                "markout_1h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 3600),
                "markout_24h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 86400),
            }
        out.append(result)
    return out


def _means(period: list[tuple[str, dict]]) -> tuple[int, float | None, float | None]:
    """
    (well-covered days, cautious mean, trades-only mean) over a run of
    finished days: income over the well-covered days, trading over the days
    a pilot ran at all (a day with no pilot neither earns nor loses).
    """
    full = [lv for _, lv in period if lv["pilot_covered"]]
    ran = [lv for _, lv in period if lv["pilot_markets"]]
    if not full:
        return 0, None, None
    income = sum(lv["pilot_income"] for lv in full) / len(full)
    return (len(full), income + sum(lv["pilot_trading"] for lv in ran) / len(ran),
            income + sum(lv.get("pilot_trading_trades_only", 0.0) for lv in ran) / len(ran))


def gate_a(rows: list[dict], level: int, today: str, settings=None) -> dict:
    """
    The go/no-go check. Rewards and rebates are averaged over the
    well-covered days, and the paper trading result over every day a pilot
    ran, covered or not. The verdict is taken once, on the finished
    day that brings the count of well-covered days to GATE_A_MIN_DAYS, and
    does not change after that: re-reading a running average every day until
    it passes would pass a losing strategy far more often. The running
    average is kept for information.
    """
    done = [(r["day"], dict(r["levels"][str(level)], plan_ok=r.get("plan_ok", True)))
            for r in rows if r["day"] < today and str(level) in r["levels"]]
    started = next((i for i, (_, lv) in enumerate(done) if lv["pilot_markets"] or lv["pilot_trading"]), len(done))
    period = done[started:]
    days, running, running_alt = _means(period)
    decided_on, mean, mean_alt, judged = None, None, None, period
    covered = 0
    for k, (day, lv) in enumerate(period):
        covered += bool(lv["pilot_covered"])
        if covered == GATE_A_MIN_DAYS:
            decided_on, judged = day, period[:k + 1]
            _, mean, mean_alt = _means(judged)
            break
    plan_ok = ((settings is None or all(getattr(settings, name) == v for name, v in PLAN.items()))
               and all(lv["plan_ok"] for _, lv in judged))
    if decided_on is None:
        verdict = "NOT ENOUGH DATA YET"
    elif not plan_ok:
        verdict = "NO VERDICT: the pilot settings differ from the plan the bar was set for"
    elif mean > GATE_A_USD_PER_DAY:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    return {"verdict": verdict, "decided_on": decided_on, "needed_days": GATE_A_MIN_DAYS,
            "threshold_usd_per_day": GATE_A_USD_PER_DAY,
            "mean_cautious_usd_per_day": mean, "mean_trades_only_usd_per_day": mean_alt,
            "days": days, "days_since_start": len(period),
            "running_cautious_usd_per_day": running, "running_trades_only_usd_per_day": running_alt}


def _recent_runs(data_dir: Path, now: float) -> list[dict]:
    rows = []
    for back in (1, 0):
        day = dt.datetime.fromtimestamp(now - back * 86400, dt.timezone.utc).strftime("%Y-%m-%d")
        rows += [r for r in _read_jsonl(data_dir / "days" / day / "runs.jsonl") if r.get("ts", 0) > now - 86400]
    return rows


def _usd(x: float | None) -> str:
    if x is None:
        return "-"
    return f"-${abs(x):.2f}" if x < 0 else f"${x:.2f}"


def build(data_dir: Path, settings, now: float, this_run: dict | None = None) -> tuple[str, dict]:
    """The report text and summary; this_run is the current run's log, not yet saved."""
    level = settings.pilot_level
    stamp = dt.datetime.fromtimestamp(now, dt.timezone.utc)
    today = stamp.strftime("%Y-%m-%d")
    rows = daily_rows(data_dir, level, now)
    gate = gate_a(rows, level, today, settings)
    runs = _recent_runs(data_dir, now) + ([this_run] if this_run else [])
    noted = sum(1 for r in runs if r.get("errors"))
    if gate["decided_on"]:
        verdict_text = (
            f"Decided on {gate['decided_on']}, the {GATE_A_MIN_DAYS}th well-covered day: the pilot markets averaged "
            f"{_usd(gate['mean_cautious_usd_per_day'])} a day on the cautious estimate, against the "
            f"{_usd(GATE_A_USD_PER_DAY)} needed. If only trades could fill paper orders (no fills from midpoint "
            f"moves alone), it would have been {_usd(gate['mean_trades_only_usd_per_day'])} a day. The verdict "
            f"does not change after that day. For information, all {gate['days']} well-covered day(s) so far "
            f"average {_usd(gate['running_cautious_usd_per_day'])} "
            f"({_usd(gate['running_trades_only_usd_per_day'])} trades only).")
    elif gate["days"]:
        verdict_text = (
            f"{gate['days']} of {GATE_A_MIN_DAYS} well-covered days so far, averaging "
            f"{_usd(gate['running_cautious_usd_per_day'])} a day on the cautious estimate "
            f"({_usd(gate['running_trades_only_usd_per_day'])} if only trades could fill paper orders). "
            f"The verdict is taken once, on the {GATE_A_MIN_DAYS}th, and needs more than "
            f"{_usd(GATE_A_USD_PER_DAY)} a day.")
    else:
        verdict_text = (f"No well-covered day recorded yet. The verdict is taken once, after {GATE_A_MIN_DAYS} "
                        f"well-covered days, and needs more than {_usd(GATE_A_USD_PER_DAY)} a day.")
    lines = [
        "# Polymarket practice mode",
        "",
        f"Paper trading only: no money, no account. Last updated {stamp:%Y-%m-%d %H:%M} UTC; "
        f"{len(runs)} run(s) in the last 24 hours, {noted} with problems noted in `runs.jsonl`.",
        "",
        f"**Go/no-go check (Gate A): {gate['verdict']}.** {verdict_text}",
        "",
        f"Pilot: the top {settings.pilot_markets} markets each day where others already quote near the middle, "
        f"${settings.budget_per_market_usd:.0f} each, orders {level} tick(s) behind the closest prices to the midpoint.",
        "",
        "| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in reversed(rows[-14:]):
        lv = r["levels"].get(str(level))
        if not lv:
            continue
        mark = " (today, so far)" if r["day"] >= today else ("" if lv["pilot_covered"] else " (partial day)")
        lines.append(
            f"| {r['day']}{mark} | {_usd(lv['pilot_cautious'])} | {_usd(lv['pilot_optimistic'])} | "
            f"{_usd(lv['pilot_rewards_low'])} | {_usd(lv['pilot_trading'])} | "
            f"{_usd(lv.get('pilot_trading_trades_only'))} | "
            f"{_usd(lv['all_rewards_low'])}-{_usd(lv['all_rewards_high'])} | {lv['fills']} | {_usd(lv['markout_1h'])} |"
        )
    lines += [
        "",
        "Other distances from the midpoint, latest full day:",
        "",
    ]
    full = [r for r in rows if r["day"] < today and r["levels"].get(str(level), {}).get("pilot_covered")]
    if full:
        last = full[-1]
        for lv_name, lv in sorted(last["levels"].items()):
            lines.append(
                f"- {lv_name} tick(s) back: pilot cautious {_usd(lv['pilot_cautious'])}, "
                f"{lv.get('all_markets', lv['markets'])} watched markets (not thin), rewards "
                f"{_usd(lv['all_rewards_low'])}-{_usd(lv['all_rewards_high'])}, "
                f"trading {_usd(lv['all_trading'])} ({_usd(lv.get('all_trading_trades_only'))} trades only), "
                f"rebates {_usd(lv['all_rebates'])}, fills {lv['fills']}, "
                f"24h markouts {_usd(lv['markout_24h'])}"
            )
        thin = last["levels"].get(str(level), {})
        if thin.get("thin_markets"):
            lines += [
                "",
                f"Thin markets ({thin['thin_markets']} watched): nobody else quotes near the middle, so a paper "
                f"order there would set the price alone and these numbers cannot be trusted. Best case rewards "
                f"{_usd(thin['thin_rewards_high'])}, paper trading {_usd(thin['thin_trading'])}. They never count "
                f"towards the go/no-go check.",
            ]
    else:
        lines.append("- No full day recorded yet.")
    summary = {"generated": int(now), "gate_a": gate, "days": rows[-REPORT_DAYS:]}
    return "\n".join(lines) + "\n", summary
