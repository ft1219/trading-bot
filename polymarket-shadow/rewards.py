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
  to at most that. On top of that, makers already inside the reward band
  are assumed to move up to our price if they are further out, because
  other reward bots would answer a better-placed order within minutes.

A market is "thin" when, on either side, other makers have less than the
minimum reward size inside the band. Our paper order would then be the
price, not a follower of it, and paper results there cannot be trusted.
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
    return round((bid + ask) / 2, 6)  # so 0.10 and 0.90 compare exactly


def raw_midpoint(book: Book) -> float | None:
    """(best bid + best ask) / 2, the midpoint Polymarket's price history records."""
    if book.best_bid is None or book.best_ask is None or book.best_bid >= book.best_ask:
        return None
    return round((book.best_bid + book.best_ask) / 2, 6)


def with_orders(book: Book, bid: float | None, ask: float | None, size: float) -> Book:
    """The book with our own orders added, as the reward sampler would see it."""
    bids = list(book.bids) + ([Level(bid, size)] if bid is not None and size > 0 else [])
    asks = list(book.asks) + ([Level(ask, size)] if ask is not None and size > 0 else [])
    return Book(tuple(sorted(bids, key=lambda l: -l.price)), tuple(sorted(asks, key=lambda l: l.price)), book.tick)


def cents(price_gap: float) -> float:
    """A price difference in cents, rounded so that a level exactly v cents away compares equal to v."""
    return round(price_gap * 100, 6)


def order_score(max_spread_c: float, distance_c: float, multiplier: float = 1.0) -> float:
    """S(v, s); zero at or beyond the max spread."""
    if max_spread_c <= 0 or distance_c < 0 or distance_c >= max_spread_c:
        return 0.0
    return ((max_spread_c - distance_c) / max_spread_c) ** 2 * multiplier


def q_min(q_one: float, q_two: float, midpoint: float) -> float:
    if TWO_SIDED_ONLY_BELOW <= midpoint <= TWO_SIDED_ONLY_ABOVE:
        return max(min(q_one, q_two), max(q_one, q_two) / SINGLE_SIDED_DIVISOR)
    return min(q_one, q_two)


def side_score(levels: tuple[Level, ...], midpoint: float, max_spread_c: float, min_level_size: float = 0.0,
               match_c: float | None = None) -> float:
    """
    Q summed over one side of the book. With match_c, every level inside the
    band scores at least as well as an order match_c cents from the midpoint.
    """
    floor = order_score(max_spread_c, match_c) if match_c is not None else 0.0
    total = 0.0
    for level in levels:
        if level.size < min_level_size:
            continue
        score = order_score(max_spread_c, cents(abs(level.price - midpoint)))
        if score > 0:
            score = max(score, floor)
        total += score * level.size
    return total


def depth_in_band(levels: tuple[Level, ...], midpoint: float, max_spread_c: float) -> float:
    return sum(l.size for l in levels if cents(abs(l.price - midpoint)) < max_spread_c)


def is_thin(book: Book, midpoint: float, max_spread_c: float, min_size: float) -> bool:
    """True when other makers leave either side of the reward band without min_size of depth (an empty band is always thin)."""
    need = max(min_size, 1e-9)
    return (depth_in_band(book.bids, midpoint, max_spread_c) < need
            or depth_in_band(book.asks, midpoint, max_spread_c) < need)


@dataclass(frozen=True)
class Competition:
    low: float
    high: float


def competition(book: Book, midpoint: float, max_spread_c: float, min_size: float,
                bid_c: float | None = None, ask_c: float | None = None) -> Competition:
    """
    Bounds on the other makers' total Q_min. bid_c and ask_c are our own
    orders' distances from the midpoint in cents: for the high bound, makers
    inside the band are moved up to them (see the module notes).
    """
    a_all = side_score(book.bids, midpoint, max_spread_c, match_c=bid_c)
    b_all = side_score(book.asks, midpoint, max_spread_c, match_c=ask_c)
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
    q_one = order_score(max_spread_c, cents(midpoint - bid)) * size if ok and bid is not None else 0.0
    q_two = order_score(max_spread_c, cents(ask - midpoint)) * size if ok and ask is not None else 0.0
    q = q_min(q_one, q_two, midpoint)
    share_low = q / (q + comp.high) if q > 0 else 0.0
    share_high = q / (q + comp.low) if q > 0 else 0.0
    return OurScore(q_one, q_two, q, share_low, share_high)


@dataclass(frozen=True)
class Scored:
    reward_mid: float | None  # size-cutoff midpoint with our orders in the book
    thin: bool
    comp: Competition
    ours: OurScore


NO_SCORE = OurScore(0.0, 0.0, 0.0, 0.0, 0.0)


def score_quotes(book: Book, bid: float | None, ask: float | None, size: float,
                 max_spread_c: float, min_size: float) -> Scored:
    """
    Our reward share for orders at bid/ask (None: not posted), measured the
    way Polymarket's sampler would see the book with our orders in it.
    """
    mid = adjusted_midpoint(with_orders(book, bid, ask, size), min_size)
    if mid is None:
        return Scored(None, True, Competition(0.0, 0.0), NO_SCORE)
    comp = competition(book, mid, max_spread_c, min_size,
                       bid_c=cents(mid - bid) if bid is not None else None,
                       ask_c=cents(ask - mid) if ask is not None else None)
    ours = our_score(bid, ask, size, mid, max_spread_c, min_size, comp)
    return Scored(mid, is_thin(book, mid, max_spread_c, min_size), comp, ours)
