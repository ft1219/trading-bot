"""
Builds the lab's report.md (written to be read on a phone) and summary.json.

The pass rule is fixed here, before any results, so it cannot drift to fit
them. A strategy is judged once, on the first run where it has been going
for JUDGE_DAYS days with at least MIN_SETTLED finished trades spread over at
least MIN_DAYS different days; that verdict is stored and never recomputed
(judging again on every run would let a lucky streak show "PASS" at some
point even with no edge). It passes if it made money overall AND its win
count is one the prices alone would produce less than once in a hundred
tries (an exact binomial test against the break-even win rate, which is the
average price paid). Before judgment day it is "too early", whatever the
numbers say. The coin_flip yardstick is shown for comparison only.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

import strategies as S

JUDGE_DAYS = 14
MIN_SETTLED = 30
MIN_DAYS = 10  # finished trades on at least this many different days (one lucky day is not evidence)
P_LUCK = 0.01  # a win count this likely by chance alone is not a pass
DAILY_ROWS = 10


def read_jsonl(path: Path) -> list[dict]:
    """Rows of one .jsonl file, or of every .jsonl file in a folder (by name)."""
    if path.is_dir():
        out = []
        for f in sorted(path.glob("*.jsonl")):
            out.extend(read_jsonl(f))
        return out
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


def binom_tail(wins: int, n: int, p: float) -> float:
    """P(X >= wins) for X ~ Binomial(n, p)."""
    if n <= 0 or wins <= 0:
        return 1.0
    if p >= 1:
        return 1.0
    if p <= 0:
        return 0.0
    lp, lq = math.log(p), math.log(1 - p)
    total = 0.0
    for k in range(wins, n + 1):
        total += math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * lp + (n - k) * lq)
    return min(1.0, total)


def stats(rows: list[dict]) -> dict:
    n = len(rows)
    staked = sum(r["cost"] for r in rows)
    pnl = sum(r["pnl"] for r in rows)
    wins = sum(1 for r in rows if r["pnl"] > 0)
    # break-even win rate: what the trades cost per dollar they would pay if won
    pays = sum(r.get("payout_if_won") or (r["cost"] + max(r["pnl"], 0.0)) for r in rows)
    p0 = staked / pays if pays else 1.0
    return {"settled": n, "wins": wins, "staked": round(staked, 2), "pnl": round(pnl, 2),
            "roi": (pnl / staked) if staked else 0.0, "break_even_rate": round(p0, 4),
            "p_luck": binom_tail(wins, n, p0) if n else 1.0,
            "days": len({_day(r["settled_at"]) for r in rows if "settled_at" in r})}


def judge(name: str, st: dict, days_running: float) -> str | None:
    """The verdict to store now, or None if it is still too early to judge."""
    cfg = S.STRATEGIES.get(name, {})
    if cfg.get("judge") == "yardstick":
        return None
    if days_running < JUDGE_DAYS:
        return None
    if st["settled"] < MIN_SETTLED:
        return "nothing to judge" if st["settled"] == 0 and days_running >= 2 * JUDGE_DAYS else None
    if st["days"] < MIN_DAYS:
        return None
    if cfg.get("judge") == "arbitrage":
        return "PASS" if st["pnl"] > 0 and st["wins"] == st["settled"] else "FAIL"
    return "PASS" if st["pnl"] > 0 and st["p_luck"] < P_LUCK else "FAIL"


def verdict(name: str, st: dict, days_running: float, stored: dict | None = None) -> str:
    """
    The verdict to show: the stored one if the strategy was already judged,
    otherwise judge it now (the caller stores a non-None result).
    """
    if S.STRATEGIES.get(name, {}).get("judge") == "yardstick":
        return "yardstick"
    if stored and stored.get("verdict"):
        return stored["verdict"]
    return judge(name, st, days_running) or "too early"


def build(data: Path, now: float, state: dict | None = None) -> tuple[str, dict]:
    trades = read_jsonl(data / "trades")
    settled = read_jsonl(data / "settled")
    runs = read_jsonl(data / "runs.jsonl")
    if state is None:
        state = json.loads((data / "state.json").read_text()) if (data / "state.json").exists() else {}
    state.setdefault("positions", [])
    verdicts = state.setdefault("verdicts", {})
    today = _day(now)

    by_s: dict[str, dict] = {}
    for name, cfg in S.STRATEGIES.items():
        mine = [r for r in settled if r["strategy"] == name]
        st = stats(mine)
        since = dt.datetime.fromisoformat(cfg["since"]).replace(tzinfo=dt.timezone.utc).timestamp()
        days_running = max(0.0, (now - since) / 86400)
        opened = [t for t in trades if t["strategy"] == name]
        still_open = [p for p in state["positions"] if p["strategy"] == name]
        if name not in verdicts:
            j = judge(name, st, days_running)
            if j:
                verdicts[name] = {"verdict": j, "at": int(now), "settled": st["settled"], "pnl": st["pnl"],
                                  "p_luck": st["p_luck"]}
        st.update({"trades": len(opened), "open": len(still_open),
                   "open_cost": round(sum(p["cost"] for p in still_open), 2),
                   "days_running": round(days_running, 1), "active": bool(cfg.get("active")),
                   "verdict": verdict(name, st, days_running, verdicts.get(name))})
        by_s[name] = st

    def rank(k):
        st = by_s[k]
        return (k == "coin_flip", st["settled"] < 10, -st["roi"] if st["settled"] >= 10 else -st["settled"])
    order = sorted(by_s, key=rank)
    lines = [
        "# Polymarket strategy lab (pretend money)",
        "",
        f"Updated {dt.datetime.fromtimestamp(now, dt.timezone.utc):%Y-%m-%d %H:%M} UTC. "
        f"Each pretend trade is ${S.STAKE_USD:.0f}, bought at the real asking price plus fees, held to the result. "
        "Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real "
        "account would make; compare strategies by \"Per $1\".",
        "",
        "## Scoreboard (finished trades only)",
        "",
        "| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, name in enumerate(order, 1):
        st = by_s[name]
        per = f"{st['roi'] * 100:+.1f}%" if st["settled"] else "-"
        won = f"{st['wins']}/{st['settled']}" if st["settled"] else "-"
        tag = "" if st["active"] else " (stopped)"
        lines.append(f"| {i} | {name}{tag} | {st['settled']} | {won} | {per} | {_usd(st['pnl'])} | {st['days']} | "
                     f"{st['open']} | {st['verdict']} |")
    lines += ["", "What each one does:", ""]
    for name in order:
        lines.append(f"- **{name}**: {S.STRATEGIES[name]['plain']}.")
    lines += [
        "",
        f"Pass rule (fixed in advance): a strategy is judged once, on the first run after {JUDGE_DAYS} days with at least "
        f"{MIN_SETTLED} finished trades on at least {MIN_DAYS} different days. It passes only if it made money AND "
        f"its number of wins is one that the prices alone would produce less than {P_LUCK * 100:.0f} time in 100 "
        "(so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, \"too early\". "
        "\"Days\" counts the different days on which its trades finished.",
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

    gaps = read_jsonl(data / "gaps" / f"{today}.jsonl")
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
    if bad:
        lines.append("Latest problem: " + str(bad[-1]["problems"][-1])[:200])

    summary = {"updated": int(now), "strategies": {k: {kk: (None if isinstance(vv, float) and math.isinf(vv) else vv)
                                                        for kk, vv in v.items()} for k, v in by_s.items()},
               "runs_24h": len(last_day), "runs_with_problems_24h": len(bad)}
    return "\n".join(lines) + "\n", summary
