"""
Turns the recorded practice data into a daily table and the go/no-go check.

Gate A (fixed before any data, in the project plan): go live with a small
pilot only if, over at least 14 well-covered days, the cautious estimate for
the pilot markets of
    liquidity rewards + maker rebates + paper trading result
averages more than $1.50 a day.

"Cautious" means: competitors are assumed as strong as the order book allows
(and to move up to our price), a thin market earns nothing, holdings are
valued at what they would sell for, and the $1 minimum payout is applied to
each market separately (it may in fact apply to the whole account, which is
the "optimistic" column).
"""
from __future__ import annotations

import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

GATE_A_USD_PER_DAY = 1.50
GATE_A_MIN_DAYS = 14
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


def daily_rows(data_dir: Path, pilot_level: int, now: float) -> list[dict]:
    days_dir = data_dir / "days"
    if not days_dir.exists():
        return []
    day_names = sorted(p.name for p in days_dir.iterdir() if p.is_dir())[-REPORT_DAYS:]
    last_value: dict[tuple[str, int], float] = {}
    last_rebates: dict[tuple[str, int], float] = {}
    out = []
    for day in day_names:
        samples = _read_jsonl(days_dir / day / "samples.jsonl")
        closeouts = _read_jsonl(days_dir / day / "closeouts.jsonl")
        fills = _read_jsonl(days_dir / day / "fills.jsonl")
        markouts = _read_jsonl(days_dir / day / "markouts.jsonl")
        per: dict[tuple[str, int], dict] = defaultdict(lambda: {"low": 0.0, "high": 0.0, "dt": 0, "value": None,
                                                                 "rebates": None, "pilot": False, "thin_dt": 0})
        trading: dict[tuple[str, int], float] = defaultdict(float)
        for c in closeouts:  # positions sold at the touch when a market left the watchlist
            key = (c["condition_id"], int(c["level"]))
            trading[key] += c["value_after"] - last_value.get(key, 0.0)
            last_value[key] = 0.0
            per[key]["pilot"] = per[key]["pilot"] or c.get("pilot", False)
            rebate_gain = c.get("rebates", 0.0) - last_rebates.get(key, 0.0)
            per[key]["closeout_rebates"] = rebate_gain
            last_rebates[key] = 0.0
        for srow in sorted(samples, key=lambda r: r["ts"]):
            for lv, d in srow["levels"].items():
                key = (srow["condition_id"], int(lv))
                agg = per[key]
                agg["low"] += d["est_low"]
                agg["high"] += d["est_high"]
                agg["dt"] += srow["dt"]
                agg["value"] = d["value"]
                agg["rebates"] = d["rebates"]
                agg["pilot"] = agg["pilot"] or srow.get("pilot", False)
                if srow.get("thin"):
                    agg["thin_dt"] += srow["dt"]
        result = {"day": day, "levels": {}}
        for level in sorted({k[1] for k in per} | {pilot_level}):
            keys = [k for k in per if k[1] == level]
            mk = []
            for key in keys:
                agg = per[key]
                coverage = agg["dt"] / 86400
                scale = 1 / coverage if coverage >= MIN_COVERAGE else 1.0
                low, high = agg["low"] * scale, agg["high"] * scale
                reb = agg.get("closeout_rebates", 0.0)
                if agg["rebates"] is not None:
                    reb += agg["rebates"] - last_rebates.get(key, 0.0)
                    last_rebates[key] = agg["rebates"]
                trade = trading.get(key, 0.0)
                if agg["value"] is not None:
                    trade += agg["value"] - last_value.get(key, 0.0)
                    last_value[key] = agg["value"]
                thin = not agg["pilot"] and agg["thin_dt"] * 2 > agg["dt"]  # thin for most of the day
                mk.append({"condition_id": key[0], "pilot": agg["pilot"], "thin": thin, "coverage": coverage,
                           "rewards_low": low, "rewards_high": high, "rebates": reb, "trading": trade})
            pilot = [x for x in mk if x["pilot"]]
            est = [x for x in mk if not x["thin"]]
            thin_mk = [x for x in mk if x["thin"]]
            sampled = [x for x in pilot if x["coverage"] > 0]  # closeout-only rows have no samples
            covered = bool(sampled) and min(x["coverage"] for x in sampled) >= MIN_COVERAGE
            result["levels"][str(level)] = {
                "markets": len(mk),
                "pilot_markets": len(pilot),
                "pilot_covered": covered,
                "pilot_cautious": sum(_floor(x["rewards_low"]) + _floor(x["rebates"]) + x["trading"] for x in pilot),
                "pilot_optimistic": _floor(sum(x["rewards_high"] for x in pilot)) + _floor(sum(x["rebates"] for x in pilot))
                + sum(x["trading"] for x in pilot),
                "pilot_rewards_low": sum(x["rewards_low"] for x in pilot),
                "pilot_trading": sum(x["trading"] for x in pilot),
                "all_markets": len(est),
                "all_rewards_low": sum(x["rewards_low"] for x in est),
                "all_rewards_high": sum(x["rewards_high"] for x in est),
                "all_rebates": sum(x["rebates"] for x in est),
                "all_trading": sum(x["trading"] for x in est),
                "thin_markets": len(thin_mk),
                "thin_rewards_high": sum(x["rewards_high"] for x in thin_mk),
                "thin_trading": sum(x["trading"] for x in thin_mk),
                "fills": sum(1 for f in fills if int(f["level"]) == level),
                "markout_1h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 3600),
                "markout_24h": sum(m["markout_usd"] for m in markouts if int(m["level"]) == level and m["horizon"] == 86400),
            }
        out.append(result)
    return out


def gate_a(rows: list[dict], level: int, today: str) -> dict:
    full = [r for r in rows if r["day"] < today and r["levels"].get(str(level), {}).get("pilot_covered")]
    values = [r["levels"][str(level)]["pilot_cautious"] for r in full]
    mean = sum(values) / len(values) if values else None
    if len(values) < GATE_A_MIN_DAYS:
        verdict = "NOT ENOUGH DATA YET"
    elif mean > GATE_A_USD_PER_DAY:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    return {"days": len(values), "needed_days": GATE_A_MIN_DAYS, "mean_cautious_usd_per_day": mean,
            "threshold_usd_per_day": GATE_A_USD_PER_DAY, "verdict": verdict}


def _usd(x: float | None) -> str:
    if x is None:
        return "-"
    return f"-${abs(x):.2f}" if x < 0 else f"${x:.2f}"


def build(data_dir: Path, settings, now: float) -> tuple[str, dict]:
    level = settings.pilot_level
    today = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")
    rows = daily_rows(data_dir, level, now)
    gate = gate_a(rows, level, today)
    lines = [
        "# Polymarket practice mode",
        "",
        "Paper trading only: no money, no account. Updated every run.",
        "",
        f"**Go/no-go check (Gate A): {gate['verdict']}.** "
        + (f"Pilot markets averaged {_usd(gate['mean_cautious_usd_per_day'])} a day on the cautious estimate over "
           f"{gate['days']} full day(s). " if gate["days"] else "No full day recorded yet. ")
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
        mark = "" if lv["pilot_covered"] else " (partial day)"
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
    full = [r for r in rows if r["day"] < today]
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
    summary = {"generated": int(now), "gate_a": gate, "days": rows}
    return "\n".join(lines) + "\n", summary
