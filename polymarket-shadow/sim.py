"""
Paper market making on one market, replayed from public trades.

We pretend to keep a bid and an ask resting around the midpoint all the time,
re-quoting each minute from Polymarket's one-minute midpoint history, and we
use every public taker trade to decide whether our orders would have filled.
The rules lean towards making us look worse than reality:

- A fill counts only when a trade prints strictly through our price. A trade
  at our price might have filled us if we were early in the queue; we
  ignore it. A trade through our price means the whole price level was
  used up, so our full order fills.
- Quotes come from the midpoint of the minute *before* the trade, so a fast
  move hits our stale quote, as it would hit a slow real bot.
- After a fill we wait for the next minute's midpoint before re-quoting.
- A per-market budget caps what we hold: resting orders lock their cost and
  bought shares keep it locked until a YES and a NO are merged back into $1.

Prices are YES-equivalent throughout: a NO bid at n is the same order as a
YES ask at 1 - n, and Polymarket matches them against each other.
"""
from __future__ import annotations

import bisect
from dataclasses import asdict, dataclass, field

import rewards

REQUOTE_DELAY_S = 60
MAX_QUOTE_AGE_S = 300  # no midpoint this recent: assume we were not quoting
EPS = 1e-9


@dataclass
class Position:
    yes: float = 0.0
    yes_cost: float = 0.0
    no: float = 0.0
    no_cost: float = 0.0
    cash: float = 0.0  # starts at 0: P&L is measured from here
    rebates: float = 0.0
    fills: int = 0
    bid_blocked_until: float = 0.0
    ask_blocked_until: float = 0.0

    def held_cost(self) -> float:
        return self.yes_cost + self.no_cost

    def value(self, mid: float) -> float:
        return self.cash + self.yes * mid + self.no * (1 - mid)

    def merge_pairs(self) -> None:
        pairs = min(self.yes, self.no)
        if pairs <= EPS:
            return
        self.yes_cost -= self.yes_cost * pairs / self.yes
        self.no_cost -= self.no_cost * pairs / self.no
        self.yes -= pairs
        self.no -= pairs
        self.cash += pairs  # each YES + NO pair redeems for $1

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Position":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})


@dataclass(frozen=True)
class MarketParams:
    tick: float
    size: float  # shares per order
    budget_usd: float
    max_spread_c: float
    fee_rate: float = 0.0
    fee_exponent: float = 1.0
    rebate_rate: float = 0.0


def active_sides(pos: Position, bid: float | None, ask: float | None, p: MarketParams, now: float) -> tuple[bool, bool]:
    """Which of our two orders can rest right now, within the budget."""
    want_bid = bid is not None and now >= pos.bid_blocked_until
    want_ask = ask is not None and now >= pos.ask_blocked_until
    lock_bid = p.size * bid if want_bid else 0.0
    lock_ask = p.size * (1 - ask) if want_ask else 0.0
    held = pos.held_cost()
    # The order that shrinks our holdings gets the budget first.
    order = ("ask", "bid") if pos.yes > pos.no else ("bid", "ask")
    used = held
    result = {"bid": False, "ask": False}
    for side in order:
        lock, want = (lock_bid, want_bid) if side == "bid" else (lock_ask, want_ask)
        if want and used + lock <= p.budget_usd + EPS:
            result[side] = True
            used += lock
    return result["bid"], result["ask"]


def in_band(mid: float, bid: float | None, ask: float | None, max_spread_c: float) -> tuple[float | None, float | None]:
    """Drop a quote that would sit outside the reward band (we would not post it)."""
    if bid is not None and (bid <= 0 or (mid - bid) * 100 >= max_spread_c):
        bid = None
    if ask is not None and (ask >= 1 or (ask - mid) * 100 >= max_spread_c):
        ask = None
    return bid, ask


def quotes(mid: float, p: MarketParams, level: int) -> tuple[float | None, float | None]:
    bid, ask = rewards.quote_prices(mid, p.tick, level)
    return in_band(mid, bid, ask, p.max_spread_c)


def taker_fee_equivalent(shares: float, price: float, p: MarketParams) -> float:
    """Polymarket's fee curve: shares * rate * (p * (1 - p)) ** exponent."""
    if p.fee_rate <= 0:
        return 0.0
    return shares * p.fee_rate * (price * (1 - price)) ** p.fee_exponent


def yes_equivalent(trade: dict, yes_token: str) -> tuple[str, float] | None:
    """(taker side on YES, YES price) for a taker trade on either token."""
    side = str(trade.get("side", "")).upper()
    price = float(trade["price"])
    if side not in ("BUY", "SELL"):
        return None
    if str(trade.get("asset")) == yes_token:
        return side, price
    # Buying NO at n is selling YES at 1 - n, and the other way round.
    return ("SELL" if side == "BUY" else "BUY"), 1 - price


@dataclass
class Fill:
    ts: int
    side: str  # "bid": we bought YES; "ask": we bought NO (sold YES)
    price: float  # YES-equivalent price of our order
    shares: float
    mid_before: float
    trade_price: float
    rebate: float
    tx: str = ""
    level: int = 0
    extra: dict = field(default_factory=dict)


def replay(pos: Position, trades: list[dict], history: list[tuple[int, float]], yes_token: str,
           p: MarketParams, level: int) -> list[Fill]:
    """Apply taker trades (oldest first) to our paper position; returns our fills."""
    times = [t for t, _ in history]
    fills: list[Fill] = []
    for trade in trades:
        ts = int(trade["timestamp"])
        i = bisect.bisect_left(times, ts) - 1  # last midpoint strictly before the trade
        if i < 0 or ts - times[i] > MAX_QUOTE_AGE_S:
            continue
        mid = history[i][1]
        converted = yes_equivalent(trade, yes_token)
        if converted is None:
            continue
        taker_side, price = converted
        bid, ask = quotes(mid, p, level)
        bid_on, ask_on = active_sides(pos, bid, ask, p, ts)
        next_quote = times[i + 1] if i + 1 < len(times) else ts + REQUOTE_DELAY_S
        if taker_side == "SELL" and bid_on and price < bid - EPS:
            pos.yes += p.size
            pos.yes_cost += p.size * bid
            pos.cash -= p.size * bid
            pos.bid_blocked_until = max(next_quote, ts + 1)
            fill_price, side = bid, "bid"
        elif taker_side == "BUY" and ask_on and price > ask + EPS:
            pos.no += p.size
            pos.no_cost += p.size * (1 - ask)
            pos.cash -= p.size * (1 - ask)
            pos.ask_blocked_until = max(next_quote, ts + 1)
            fill_price, side = ask, "ask"
        else:
            continue
        rebate = p.rebate_rate * taker_fee_equivalent(p.size, fill_price, p)
        pos.rebates += rebate
        pos.fills += 1
        pos.merge_pairs()
        fills.append(Fill(ts=ts, side=side, price=fill_price, shares=p.size, mid_before=mid,
                          trade_price=price, rebate=rebate, tx=str(trade.get("transactionHash", "")), level=level))
    return fills


def close_out(pos: Position, best_bid: float | None, best_ask: float | None) -> float:
    """Sell what we hold at the touch (YES at the bid, NO at 1 - ask). Returns cash received."""
    received = 0.0
    if pos.yes > EPS and best_bid is not None:
        received += pos.yes * best_bid
        pos.yes, pos.yes_cost = 0.0, 0.0
    if pos.no > EPS and best_ask is not None:
        received += pos.no * (1 - best_ask)
        pos.no, pos.no_cost = 0.0, 0.0
    pos.cash += received
    return received


def markout(fill_side: str, fill_price: float, later_mid: float, shares: float) -> float:
    """Dollar gain of a fill if valued at a later midpoint (negative: the market moved against us)."""
    if fill_side == "bid":
        return (later_mid - fill_price) * shares
    return (fill_price - later_mid) * shares
