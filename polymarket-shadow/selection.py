"""
Choosing which reward markets to watch, using only what is known at the time.

Every day the recorder picks a watchlist from all markets in the liquidity
rewards program, and marks the top few as the "pilot" markets: the ones a
real pilot with a small budget would have quoted. The go/no-go decision is
based on the pilot markets only, chosen before their results are known, so
the result is not flattered by picking winners afterwards.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass

import rewards


@dataclass(frozen=True)
class Settings:
    budget_per_market_usd: float = 20.0
    watch_markets: int = 25
    pilot_markets: int = 2
    pilot_level: int = 1  # ticks behind the closest prices; fixed in advance
    min_daily_rate_usd: float = 10.0
    min_days_to_end: float = 7.0
    min_mid: float = 0.15
    max_mid: float = 0.85
    books_to_check: int = 120


@dataclass
class Candidate:
    condition_id: str
    question: str
    yes_token: str
    no_token: str
    end_date: str | None
    neg_risk: bool
    tick: float
    order_min: float
    min_size: float
    max_spread_c: float
    daily_rate: float
    mid: float | None = None
    size: float = 0.0
    expected_low: float = 0.0  # $/day for us at pilot_level with competitors at their high bound
    expected_high: float = 0.0
    fee_rate: float = 0.0
    fee_exponent: float = 1.0
    rebate_rate: float = 0.0
    pilot: bool = False
    rank: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def _parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def prefilter(sampling: list[dict], configs: dict[str, dict], now: dt.datetime, s: Settings) -> list[Candidate]:
    """Cheap filters on the market lists, before fetching any books."""
    out: list[Candidate] = []
    for m in sampling:
        cid = m.get("condition_id")
        cfg = configs.get(cid or "")
        if not cid or not cfg:
            continue
        if not (m.get("active") and m.get("accepting_orders") and m.get("enable_order_book", True)) or m.get("closed"):
            continue
        if m.get("game_start_time") or (m.get("seconds_delay") or 0) > 0:
            continue  # live sports: in-game rules and delays we do not model
        tokens = m.get("tokens") or []
        if len(tokens) != 2:
            continue
        yes = next((t for t in tokens if str(t.get("outcome", "")).lower() == "yes"), tokens[0])
        no = next(t for t in tokens if t is not yes)
        try:
            price = float(yes.get("price"))
            rate = float(cfg.get("total_daily_rate") or cfg.get("native_daily_rate") or 0)
            min_size = float(cfg.get("rewards_min_size") or 0)
            max_spread = float(cfg.get("rewards_max_spread") or 0)
            tick = float(m.get("minimum_tick_size") or 0.01)
        except (TypeError, ValueError):
            continue
        if rate < s.min_daily_rate_usd or max_spread <= 0 or not (s.min_mid <= price <= s.max_mid):
            continue
        if min_size > s.budget_per_market_usd:  # a two-sided pair of min-size orders costs about min_size dollars
            continue
        end = _parse_time(m.get("end_date_iso"))
        if end is None or (end - now).total_seconds() < s.min_days_to_end * 86400:
            continue
        out.append(Candidate(
            condition_id=cid, question=str(m.get("question", ""))[:140],
            yes_token=str(yes["token_id"]), no_token=str(no["token_id"]),
            end_date=m.get("end_date_iso"), neg_risk=bool(m.get("neg_risk")),
            tick=tick, order_min=float(m.get("minimum_order_size") or 5),
            min_size=min_size, max_spread_c=max_spread, daily_rate=rate,
        ))
    out.sort(key=lambda c: -c.daily_rate)
    return out


def order_size(c: Candidate, bid: float, ask: float, budget: float) -> float:
    """Shares per order: as many as the budget allows for one bid and one ask."""
    pair_cost = bid + (1 - ask)
    if pair_cost <= 0:
        return 0.0
    size = float(int(budget / pair_cost))
    return size if size >= max(c.min_size, c.order_min) else 0.0


def score_candidates(cands: list[Candidate], books: dict[str, dict], s: Settings) -> list[Candidate]:
    """Expected reward per day for each candidate from its live book."""
    scored: list[Candidate] = []
    for c in cands:
        raw = books.get(c.yes_token)
        if not raw:
            continue
        book = rewards.parse_book(raw)
        mid = rewards.adjusted_midpoint(book, c.min_size)
        if mid is None or not (s.min_mid <= mid <= s.max_mid):
            continue
        bid, ask = rewards.quote_prices(mid, book.tick, s.pilot_level)
        c.tick = book.tick
        size = order_size(c, bid, ask, s.budget_per_market_usd)
        if size <= 0:
            continue
        comp = rewards.competition(book, mid, c.max_spread_c, c.min_size)
        ours = rewards.our_score(bid, ask, size, mid, c.max_spread_c, c.min_size, comp)
        if ours.q_min <= 0:
            continue
        c.mid, c.size = mid, size
        c.expected_low = c.daily_rate * ours.share_low
        c.expected_high = c.daily_rate * ours.share_high
        scored.append(c)
    scored.sort(key=lambda c: -c.expected_low)
    return scored


def apply_fees(c: Candidate, gamma: dict | None) -> None:
    """Fee curve and maker-rebate share from the Gamma market (fee-free if absent)."""
    if not gamma or not gamma.get("feesEnabled"):
        return
    sched = gamma.get("feeSchedule") or {}
    try:
        c.fee_rate = float(sched.get("rate") or 0)
        c.fee_exponent = float(sched.get("exponent") or 1)
        c.rebate_rate = float(sched.get("rebateRate") or 0)
    except (TypeError, ValueError):
        c.fee_rate = c.rebate_rate = 0.0


def choose(scored: list[Candidate], s: Settings) -> list[Candidate]:
    chosen = scored[: s.watch_markets]
    for i, c in enumerate(chosen):
        c.rank = i + 1
        c.pilot = i < s.pilot_markets
    return chosen
