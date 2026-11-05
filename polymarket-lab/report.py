"""
Builds the lab's report.md (written to be read on a phone) and summary.json.

The pass rule is fixed here, before any results, so it cannot drift to fit
them: a strategy is judged only after JUDGE_DAYS days and MIN_SETTLED
finished trades. It passes if it made money overall AND its average return
per trade stays above zero even after allowing for luck (average minus two
standard errors), AND it did better than the coin_flip yardstick. Anything
else at that point is a fail. Before that it is "too early", whatever the
numbers say.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

import strategies as S

JUDGE_DAYS = 14
MIN_SETTLED = 30
DAILY_ROWS = 10


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _day(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d")


def _usd(x: float) -> str:
    return f"{'-' if x < 0 else '+'}${abs(x):.2f}"


def stats(rows: list[dict]) -> dict:
    n = len(rows)
    staked = sum(r["cost"] for r in rows)
    pnl = sum(r["pnl"] for r in rows)
    rets = [r["pnl"] / r["cost"] for r in rows if r["cost"] > 0]
    mean = sum(rets) / len(rets) if rets else 0.0
    if len(rets) > 1:
        var = sum((x - mean) ** 2 for x in rets) / (len(rets) - 1)
        se = math.sqrt(var / len(rets))
    else:
        se = float("inf") if rets else 0.0
    return {"settled": n, "wins": sum(1 for r in rows if r["pnl"] > 0), "staked": round(staked, 2),
            "pnl": round(pnl, 2), "roi": (pnl / staked) if staked else 0.0, "mean": mean, "se": se}


def verdict(name: str, st: dict, days: float, yardstick_roi: float | None) -> str:
    if name == "coin_flip":
        return "yardstick"
    if days < JUDGE_DAYS or st["settled"] < MIN_SETTLED:
        return "too early"
    beats = yardstick_roi is None or st["roi"] > yardstick_roi
    if st["pnl"] > 0 and st["mean"] - 2 * st["se"] > 0 and beats:
        return "PASS"
    return "FAIL"


def build(data: Path, now: float) -> tuple[str, dict]:
    trades = _read_jsonl(data / "trades.jsonl")
    settled = _read_jsonl(data / "settled.jsonl")
    runs = _read_jsonl(data / "runs.jsonl")
    state = json.loads((data / "state.json").read_text()) if (data / "state.json").exists() else {"positions": []}
    today = _day(now)

    by_s: dict[str, dict] = {}
    yard = stats([r for r in settled if r["strategy"] == "coin_flip"])
    for name, cfg in S.STRATEGIES.items():
        mine = [r for r in settled if r["strategy"] == name]
        st = stats(mine)
        since = dt.datetime.fromisoformat(cfg["since"]).replace(tzinfo=dt.timezone.utc).timestamp()
        days = max(0.0, (now - since) / 86400)
        opened = [t for t in trades if t["strategy"] == name]
        still_open = [p for p in state["positions"] if p["strategy"] == name]
        st.update({"trades": len(opened), "open": len(still_open),
                   "open_cost": round(sum(p["cost"] for p in still_open), 2),
                   "days": round(days, 1), "active": bool(cfg.get("active")),
                   "verdict": verdict(name, st, days, yard["roi"] if yard["settled"] >= MIN_SETTLED else None)})
        by_s[name] = st

    order = sorted(by_s, key=lambda k: (k == "coin_flip", -by_s[k]["pnl"]))
    lines = [
        "# Polymarket strategy lab (pretend money)",
        "",
        f"Updated {dt.datetime.fromtimestamp(now, dt.timezone.utc):%Y-%m-%d %H:%M} UTC. "
        f"Each pretend trade is ${S.STAKE_USD:.0f}, bought at the real asking price plus fees, held to the result.",
        "",
        "## Scoreboard (finished trades only)",
        "",
        "| # | Strategy | Finished | Won | Profit | Per $1 | Open | Verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, name in enumerate(order, 1):
        st = by_s[name]
        per = f"{st['roi'] * 100:+.1f}%" if st["settled"] else "-"
        won = f"{st['wins']}/{st['settled']}" if st["settled"] else "-"
        tag = "" if st["active"] else " (stopped)"
        lines.append(f"| {i} | {name}{tag} | {st['settled']} | {won} | {_usd(st['pnl'])} | {per} | {st['open']} | {st['verdict']} |")
    lines += ["", "What each one does:", ""]
    for name in order:
        lines.append(f"- **{name}**: {S.STRATEGIES[name]['plain']}.")
    lines += [
        "",
        f"Pass rule (fixed in advance): after {JUDGE_DAYS} days and at least {MIN_SETTLED} finished trades, "
        "a strategy passes only if it made money, its result is still above zero after allowing for luck "
        "(average minus 2 standard errors), and it beat the coin_flip yardstick. Before that, \"too early\".",
        "",
        "## Profit by day (trades that finished that day)",
        "",
    ]
    days = sorted({_day(r["settled_at"]) for r in settled}, reverse=True)[:DAILY_ROWS]
    names = [n for n in order if any(r["strategy"] == n for r in settled)]
    if days and names:
        lines.append("| Day | " + " | ".join(names) + " |")
        lines.append("|---|" + "---|" * len(names))
        for d in days:
            cells = []
            for n in names:
                rows = [r for r in settled if r["strategy"] == n and _day(r["settled_at"]) == d]
                cells.append(_usd(sum(r["pnl"] for r in rows)) if rows else "")
            lines.append(f"| {d} | " + " | ".join(cells) + " |")
    else:
        lines.append("No trades have finished yet.")

    recent = sorted(trades, key=lambda t: -t["opened_at"])[:12]
    lines += ["", "## Latest pretend buys", ""]
    for t in recent:
        leg = t["legs"][0]
        what = t["title"] if t["strategy"] == "price_gap" else f"{t['title']} -> {leg['outcome']}"
        lines.append(f"- {_day(t['opened_at'])} {t['strategy']}: {what} at {t['avg_price']:.3f} (${t['cost']:.2f})")
    if not recent:
        lines.append("None yet.")

    gaps = _read_jsonl(data / "gaps" / f"{today}.jsonl")
    lines += ["", "## Price gaps seen today", ""]
    if gaps:
        best = min(gaps, key=lambda g: g["cost_per_set"] / g["pays"])
        lines.append(f"{len(gaps)} checks of multi-choice markets. Cheapest full set: {best['event']} "
                     f"({best['side']}), {best['cost_per_set']:.3f} for a ${best['pays']:.0f} payout.")
    else:
        lines.append("No near-gaps today.")

    last_day = [r for r in runs if r["at"] > now - 86400]
    bad = [r for r in last_day if r.get("problems")]
    lines += ["", f"Runs in the last 24 hours: {len(last_day)} ({len(bad)} with a problem)."]

    summary = {"updated": int(now), "strategies": {k: {kk: (None if isinstance(vv, float) and math.isinf(vv) else vv)
                                                        for kk, vv in v.items()} for k, v in by_s.items()},
               "runs_24h": len(last_day), "runs_with_problems_24h": len(bad)}
    return "\n".join(lines) + "\n", summary
