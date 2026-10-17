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

        # (condition_id, level, counted as pilot) -> the day's totals
        per: dict[tuple[str, int, bool], dict] = defaultdict(
            lambda: {"low": 0.0, "high": 0.0, "dt": 0, "thin_dt": 0, "rebates": 0.0, "trading": 0.0,
                     "closeout_thin": False})
        events = [(c["ts"], 0, c) for c in closeouts] + [(r["ts"], 1, r) for r in samples]
        for _, kind, row in sorted(events, key=lambda e: (e[0], e[1])):
            role = bool(row.get("pilot", False))
            if kind == 0:  # a paper position sold off when the market left the list or changed role
                key = (row["condition_id"], int(row["level"]))
                agg = per[key + (role,)]
                agg["trading"] += row["value_after"] - last_value.get(key, 0.0)
                agg["rebates"] += row.get("rebates", 0.0) - last_rebates.get(key, 0.0)
                agg["closeout_thin"] = bool(row.get("thin"))
                last_value[key] = last_rebates[key] = 0.0
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

        result = {"day": day, "levels": {}}
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
                           "rebates": agg["rebates"], "trading": agg["trading"]})
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
                "all_markets": len({x["condition_id"] for x in est}),
                "all_rewards_low": sum(x["rewards_low"] for x in est),
                "all_rewards_high": sum(x["rewards_high"] for x in est),
                "all_rebates": sum(x["rebates"] for x in est),
                "all_trading": sum(x["trading"] for x in est),
                "thin_markets": len({x["condition_id"] for x in thin_mk}),
                "thin_rewards_high": sum(x["rewards_high"] for x in thin_mk),
                "thin_trading": sum(x["trading"] for x in thin_mk),
                "fills": sum(1 for f in fills if int(f["level"]) == level),
                "markout_1h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 3600),
                "markout_24h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 86400),
            }
        out.append(result)
    return out


def gate_a(rows: list[dict], level: int, today: str, settings=None) -> dict:
    """
    The go/no-go check over every finished day: rewards and rebates averaged
    over the well-covered days, plus the paper trading result averaged over
    every day since the pilot first held a position.
    """
    done = [r["levels"][str(level)] for r in rows if r["day"] < today and str(level) in r["levels"]]
    started = next((i for i, lv in enumerate(done) if lv["pilot_markets"] or lv["pilot_trading"]), len(done))
    period = done[started:]
    full = [lv for lv in period if lv["pilot_covered"]]
    mean = None
    if full:
        income = sum(lv["pilot_income"] for lv in full) / len(full)
        mean = income + sum(lv["pilot_trading"] for lv in period) / len(period)
    plan_ok = settings is None or all(getattr(settings, k) == v for k, v in PLAN.items())
    if len(full) < GATE_A_MIN_DAYS:
        verdict = "NOT ENOUGH DATA YET"
    elif not plan_ok:
        verdict = "NO VERDICT: the pilot settings differ from the plan the bar was set for"
    elif mean > GATE_A_USD_PER_DAY:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    return {"days": len(full), "days_since_start": len(period), "needed_days": GATE_A_MIN_DAYS,
            "mean_cautious_usd_per_day": mean, "threshold_usd_per_day": GATE_A_USD_PER_DAY, "verdict": verdict}


def _usd(x: float | None) -> str:
    if x is None:
        return "-"
    return f"-${abs(x):.2f}" if x < 0 else f"${x:.2f}"


def build(data_dir: Path, settings, now: float) -> tuple[str, dict]:
    level = settings.pilot_level
    today = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")
    rows = daily_rows(data_dir, level, now)
    gate = gate_a(rows, level, today, settings)
    lines = [
        "# Polymarket practice mode",
        "",
        "Paper trading only: no money, no account. Updated every run.",
        "",
        f"**Go/no-go check (Gate A): {gate['verdict']}.** "
        + (f"Pilot markets averaged {_usd(gate['mean_cautious_usd_per_day'])} a day on the cautious estimate over "
           f"{gate['days']} full day(s) (paper trading over all {gate['days_since_start']} day(s)). "
           if gate["days"] else "No full day recorded yet. ")
        + f"It needs more than {_usd(GATE_A_USD_PER_DAY)} a day over at least {GATE_A_MIN_DAYS} days.",
        "",
        f"Pilot: the top {settings.pilot_markets} markets each day where others already quote near the middle, "
        f"${settings.budget_per_market_usd:.0f} each, orders {level} tick(s) behind the closest prices to the midpoint.",
        "",
        "| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Watched markets (not thin), rewards low-high | Fills | 1h markouts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in reversed(rows[-14:]):
        lv = r["levels"].get(str(level))
        if not lv:
            continue
        mark = " (today, so far)" if r["day"] >= today else ("" if lv["pilot_covered"] else " (partial day)")
        lines.append(
            f"| {r['day']}{mark} | {_usd(lv['pilot_cautious'])} | {_usd(lv['pilot_optimistic'])} | "
            f"{_usd(lv['pilot_rewards_low'])} | {_usd(lv['pilot_trading'])} | "
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
                f"trading {_usd(lv['all_trading'])}, rebates {_usd(lv['all_rebates'])}, fills {lv['fills']}, "
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
