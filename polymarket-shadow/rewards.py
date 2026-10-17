"""
Polymarket liquidity-reward scoring, applied to a public order book.

From Polymarket's Liquidity Rewards docs:
- Order score S(v, s) = ((v - s) / v)^2 * b, where v is the market's max
  spread in cents, s is the order's distance in cents from the size-cutoff
  adjusted midpoint, and b is an in-game multiplier (1 outside live sports,
  which we never quote).
- Q_one adds S * size over bids on YES and asks on NO; Q_two adds asks on YES
  and bids on NO. The YES and NO books are mirror images, so the YES book's
  bids give Q_one and its asks give Q_two.
- Q_min = max(min(Q_one, Q_two), max(Q_one, Q_two) / 3) while the midpoint
  is within [0.10, 0.90]; outside that range Q_min = min(Q_one, Q_two).
- The book is sampled every minute; each day's pool is split in proportion
  to each maker's Q_min summed over the day's samples.

The public book adds up every maker's orders at a price, so the competitors'
total Q_min cannot be read exactly. It is bounded instead:
- low (good for us): only price levels at least min_size deep count, and
  every competitor quotes one side, so their total is max(A, B) / 3;
- high (bad for us): every level counts and competitors are as two-sided as
  possible, giving (A + B + min(A, B)) / 3, where A and B are the Q_one and
  Q_two totals. For each maker Q_min <= (a + b + min(a, b)) / 3, which sums
  to at most that.
"""
from __future__ import annotations

from dataclasses import dataclass

SINGLE_SIDED_DIVISOR = 3.0
TWO_SIDED_ONLY_BELOW = 0.10
TWO_SIDED_ONLY_ABOVE = 0.90


@dataclass(frozen=True)
class Level:
    price: float
    size: float


@dataclass(frozen=True)
class Book:
    bids: tuple[Level, ...]  # best (highest) first
    asks: tuple[Level, ...]  # best (lowest) first
    tick: float

    @property
    def best_bid(self) -> float | None:
        return self.bids[0].price if self.bids else None

    @property
    def best_ask(self) -> float | None:
        return self.asks[0].price if self.asks else None


def parse_book(raw: dict) -> Book:
    """CLOB book JSON (bids lowest-first, asks highest-first, strings) -> Book."""
    bids = sorted((Level(float(x["price"]), float(x["size"])) for x in raw.get("bids") or []), key=lambda l: -l.price)
    asks = sorted((Level(float(x["price"]), float(x["size"])) for x in raw.get("asks") or []), key=lambda l: l.price)
    tick = float(raw.get("tick_size") or 0.01)
    return Book(tuple(l for l in bids if l.size > 0), tuple(l for l in asks if l.size > 0), tick)


def _cutoff_price(levels: tuple[Level, ...], min_size: float) -> float | None:
    """Price where depth from the top of the book first reaches min_size."""
    depth = 0.0
    for level in levels:
        depth += level.size
        if depth >= min_size:
            return level.price
    return None


def adjusted_midpoint(book: Book, min_size: float) -> float | None:
    """
    Midpoint after ignoring dust at the top of the book: each side's price is
    where its cumulative depth first reaches min_size.
    """
    bid = _cutoff_price(book.bids, min_size)
    ask = _cutoff_price(book.asks, min_size)
    if bid is None or ask is None or bid >= ask:
        return None
    return (bid + ask) / 2


def order_score(max_spread_c: float, distance_c: float, multiplier: float = 1.0) -> float:
    """S(v, s); zero at or beyond the max spread."""
    if max_spread_c <= 0 or distance_c < 0 or distance_c >= max_spread_c:
        return 0.0
    return ((max_spread_c - distance_c) / max_spread_c) ** 2 * multiplier


def q_min(q_one: float, q_two: float, midpoint: float) -> float:
    if TWO_SIDED_ONLY_BELOW <= midpoint <= TWO_SIDED_ONLY_ABOVE:
        return max(min(q_one, q_two), max(q_one, q_two) / SINGLE_SIDED_DIVISOR)
    return min(q_one, q_two)


def side_score(levels: tuple[Level, ...], midpoint: float, max_spread_c: float, min_level_size: float = 0.0) -> float:
    total = 0.0
    for level in levels:
        if level.size < min_level_size:
            continue
        total += order_score(max_spread_c, abs(level.price - midpoint) * 100) * level.size
    return total


@dataclass(frozen=True)
class Competition:
    low: float
    high: float


def competition(book: Book, midpoint: float, max_spread_c: float, min_size: float) -> Competition:
    a_all = side_score(book.bids, midpoint, max_spread_c)
    b_all = side_score(book.asks, midpoint, max_spread_c)
    a_big = side_score(book.bids, midpoint, max_spread_c, min_level_size=min_size)
    b_big = side_score(book.asks, midpoint, max_spread_c, min_level_size=min_size)
    if TWO_SIDED_ONLY_BELOW <= midpoint <= TWO_SIDED_ONLY_ABOVE:
        low = max(a_big, b_big) / SINGLE_SIDED_DIVISOR
        high = (a_all + b_all + min(a_all, b_all)) / SINGLE_SIDED_DIVISOR
    else:
        # Only two-sided liquidity scores here; one-sided makers get nothing.
        low = 0.0
        high = min(a_all, b_all)
    return Competition(low=low, high=high)


def quote_prices(midpoint: float, tick: float, level: int) -> tuple[float, float]:
    """
    Our YES bid and YES ask `level` ticks behind the closest prices that do
    not cross the midpoint. (A NO bid at 1 - ask is the same order as a YES
    ask; Polymarket matches them against each other.)
    """
    steps_below = int((midpoint - 1e-9) / tick)  # last tick strictly below mid
    steps_above = int(-(-(midpoint + 1e-9) // tick))  # first tick strictly above mid
    bid = round((steps_below - level) * tick, 6)
    ask = round((steps_above + level) * tick, 6)
    return bid, ask


@dataclass(frozen=True)
class OurScore:
    q_one: float
    q_two: float
    q_min: float
    share_low: float  # our share if competitors are at their high bound
    share_high: float  # our share if competitors are at their low bound


def our_score(bid: float | None, ask: float | None, size: float, midpoint: float,
              max_spread_c: float, min_size: float, comp: Competition) -> OurScore:
    """Score of our hypothetical orders; pass None for a side we are not quoting."""
    ok = size >= min_size
    q_one = order_score(max_spread_c, (midpoint - bid) * 100) * size if ok and bid is not None else 0.0
    q_two = order_score(max_spread_c, (ask - midpoint) * 100) * size if ok and ask is not None else 0.0
    q = q_min(q_one, q_two, midpoint)
    share_low = q / (q + comp.high) if q > 0 else 0.0
    share_high = q / (q + comp.low) if q > 0 else 0.0
    return OurScore(q_one, q_two, q, share_low, share_high)
