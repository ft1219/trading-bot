"""
Paper market making on one market, replayed from public trade records.

We pretend to keep a bid and an ask resting near the midpoint all the time,
placing a fresh quote each minute from Polymarket's one-minute midpoint
history, and use every public trade to decide whether our orders would have
filled. The rules lean towards making us look worse than reality:

- A trade record names each order that traded and its own price. Every
  resting order that traded at a price worse than ours (a bid below our bid,
  an ask above our ask) would have traded with us first, so those shares
  fill our order, up to its size. Shares traded exactly at our price are
  ignored: we might have been behind others in the queue.
- When the midpoint itself moves through our price, whatever is left of the
  order fills at our price, even with no trade: a resting order the market
  moves past gets picked off. These fills earn no fee rebate.
- Quotes come from the midpoint of the minute *before* each event, so a fast
  move hits our stale quote, as it would hit a slow real bot. A filled order
  is only replaced, at full size, at the next minute's midpoint.
- A per-market budget caps what we hold. A bid locks its cost and an ask
  locks the cost of minting what it would sell, except the part covered by
  shares we already hold (selling YES we own needs no cash). Bought shares
  keep their cost locked until a YES and a NO are merged back into $1.
- Holdings are valued at what selling them into the current book would
  fetch, level by level, after Polymarket's taker fee.

Prices are YES-equivalent throughout: a NO bid at n is the same order as a
YES ask at 1 - n, and Polymarket matches them against each other.
"""
from __future__ import annotations

import bisect
from dataclasses import asdict, dataclass, field

import rewards

REQUOTE_DELAY_S = 60
MAX_QUOTE_AGE_S = 600  # no midpoint this recent: assume we were not quoting (the caller marks a gap)
EPS = 1e-9
# Trade prices are USDC / shares, each rounded to 6 decimals, so a trade at a
# tick can print a few millionths off it. Ticks are at least 0.001 apart.
PRICE_TOL = 1e-5


@dataclass
class Position:
    yes: float = 0.0
    yes_cost: float = 0.0
    no: float = 0.0
    no_cost: float = 0.0
    cash: float = 0.0  # starts at 0: P&L is measured from here
    rebates: float = 0.0
    fills: int = 0
    # The order resting on each side: the midpoint time it was quoted from,
    # and how many of its shares have not filled yet.
    bid_quote_ts: float = -1.0
    bid_left: float = 0.0
    ask_quote_ts: float = -1.0
    ask_left: float = 0.0

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


def active_sides(pos: Position, bid: float | None, ask: float | None, p: MarketParams,
                 bid_shares: float | None = None, ask_shares: float | None = None) -> tuple[bool, bool]:
    """Which of our two orders can rest, within the budget (default: full-size orders)."""
    bid_shares = p.size if bid_shares is None else bid_shares
    ask_shares = p.size if ask_shares is None else ask_shares
    want_bid = bid is not None and bid_shares > EPS
    want_ask = ask is not None and ask_shares > EPS
    # Buying YES while holding NO, or selling YES while holding YES, needs no cash for the covered part.
    lock_bid = max(0.0, bid_shares - pos.no) * bid if want_bid else 0.0
    lock_ask = max(0.0, ask_shares - pos.yes) * (1 - ask) if want_ask else 0.0
    # The order that shrinks our holdings gets the budget first.
    order = ("ask", "bid") if pos.yes > pos.no else ("bid", "ask")
    used = pos.held_cost()
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


def leg_side(record: dict, yes_token: str) -> tuple[str, float] | None:
    """
    ("bid" or "ask" on YES, YES price) for one order in a trade record.
    Buying NO at n is selling YES at 1 - n, and selling NO is buying YES.
    """
    side = str(record.get("side", "")).upper()
    if side not in ("BUY", "SELL"):
        return None
    price = float(record["price"])
    if str(record.get("token_id")) == yes_token:
        return ("bid" if side == "BUY" else "ask"), price
    return ("ask" if side == "BUY" else "bid"), 1 - price


@dataclass
class Fill:
    ts: int
    side: str  # "bid": we bought YES; "ask": we bought NO (sold YES)
    price: float  # YES-equivalent price of our order
    shares: float
    mid_before: float
    trade_price: float  # the worst price traded past ours, or the new midpoint
    rebate: float
    tx: str = ""
    level: int = 0
    extra: dict = field(default_factory=dict)


def _events(records: list[dict], times: list[int], start: float | None, end: float | None) -> list[tuple]:
    """Trades grouped by transaction, and midpoint updates inside (start, end], in time order."""
    groups: dict[str, list[dict]] = {}
    for n, r in enumerate(records):
        groups.setdefault(str(r.get("transaction_hash") or f"row{n}"), []).append(r)
    events = [(min(int(r["timestamp"]) for r in rs), 0, tx, rs) for tx, rs in groups.items()]
    lo = float("-inf") if start is None else start
    hi = float("inf") if end is None else end
    events += [(times[j], 1, "midpoint-move", j) for j in range(1, len(times)) if lo < times[j] <= hi]
    events.sort(key=lambda e: (e[0], e[1], e[2]))  # a trade in the same second as a new midpoint goes first
    return events


def _fill(pos: Position, side: str, price: float, shares: float) -> None:
    if side == "bid":
        pos.yes += shares
        pos.yes_cost += shares * price
        pos.cash -= shares * price
        pos.bid_left -= shares
    else:
        pos.no += shares
        pos.no_cost += shares * (1 - price)
        pos.cash -= shares * (1 - price)
        pos.ask_left -= shares
    pos.fills += 1


def replay(pos: Position, records: list[dict], history: list[tuple[int, float]], yes_token: str,
           p: MarketParams, level: int, start: float | None = None, end: float | None = None,
           stats: dict | None = None) -> list[Fill]:
    """
    Apply trade records (every party's leg, oldest first) and midpoint moves
    to our paper position; returns our fills. Midpoint moves count only
    inside (start, end], so consecutive runs do not count the same move twice.
    stats["unquoted_trades"] counts trades skipped for want of a recent midpoint.
    """
    times = [t for t, _ in history]
    fills: list[Fill] = []
    for ts, kind, tx, item in _events(records, times, start, end):
        if kind == 0:
            i = bisect.bisect_left(times, ts) - 1  # last midpoint strictly before the trade
        else:
            i = item - 1  # the quote that rested until this midpoint arrived
        if i < 0 or ts - times[i] > MAX_QUOTE_AGE_S:
            if kind == 0 and stats is not None:
                stats["unquoted_trades"] = stats.get("unquoted_trades", 0) + 1
            continue
        mid = history[i][1]
        bid, ask = quotes(mid, p, level)
        if pos.bid_quote_ts != times[i]:  # a fresh quote replaces whatever was left of the old one
            pos.bid_quote_ts, pos.bid_left = times[i], p.size
        if pos.ask_quote_ts != times[i]:
            pos.ask_quote_ts, pos.ask_left = times[i], p.size
        bid_on, ask_on = active_sides(pos, bid, ask, p, pos.bid_left, pos.ask_left)

        wanted = []  # (side, our price, shares traded past us, worst price traded)
        if kind == 0:
            legs = []
            for r in item:
                leg = leg_side(r, yes_token)
                if leg and float(r.get("size") or 0) > 0:
                    legs.append((leg[0], leg[1], float(r["size"])))
            if bid_on:
                past = [(px, sz) for s, px, sz in legs if s == "bid" and px < bid - PRICE_TOL]
                if past:
                    wanted.append(("bid", bid, sum(sz for _, sz in past), min(px for px, _ in past)))
            if ask_on:
                past = [(px, sz) for s, px, sz in legs if s == "ask" and px > ask + PRICE_TOL]
                if past:
                    wanted.append(("ask", ask, sum(sz for _, sz in past), max(px for px, _ in past)))
        else:
            new_mid = history[item][1]
            if bid_on and new_mid < bid - EPS:
                wanted.append(("bid", bid, pos.bid_left, new_mid))
            if ask_on and new_mid > ask + EPS:
                wanted.append(("ask", ask, pos.ask_left, new_mid))

        for side, price, available, worst in wanted:
            left = pos.bid_left if side == "bid" else pos.ask_left
            shares = min(left, available)
            if shares <= EPS:
                continue
            _fill(pos, side, price, shares)
            rebate = p.rebate_rate * taker_fee_equivalent(shares, price, p) if kind == 0 else 0.0
            pos.rebates += rebate
            pos.merge_pairs()
            fills.append(Fill(ts=ts, side=side, price=price, shares=shares, mid_before=mid,
                              trade_price=worst, rebate=rebate, tx=tx, level=level))
    return fills


def exit_proceeds(levels: tuple[rewards.Level, ...] | None, shares: float, p: MarketParams,
                  no_side: bool = False) -> tuple[float, float]:
    """
    Cash from selling `shares` into the book, best price first, after the
    taker fee; returns (cash, shares that found no buyer). YES sells into the
    bids; NO sells into the asks, at 1 - ask.
    """
    cash, left = 0.0, shares
    for level in levels or ():
        if left <= EPS:
            break
        take = min(left, level.size)
        px = 1 - level.price if no_side else level.price
        cash += take * px - taker_fee_equivalent(take, px, p)
        left -= take
    return cash, max(left, 0.0)


def liquidation_value(pos: Position, book: rewards.Book | None, p: MarketParams) -> float:
    """Cash plus what our holdings would fetch if sold into the book now; unsold shares count as 0."""
    yes_cash, _ = exit_proceeds(book.bids if book else None, pos.yes, p)
    no_cash, _ = exit_proceeds(book.asks if book else None, pos.no, p, no_side=True)
    return pos.cash + yes_cash + no_cash


def close_out(pos: Position, book: rewards.Book | None, p: MarketParams) -> float:
    """Sell what we hold into the book. Returns cash received; shares nobody would buy stay held."""
    yes_cash, yes_left = exit_proceeds(book.bids if book else None, pos.yes, p)
    no_cash, no_left = exit_proceeds(book.asks if book else None, pos.no, p, no_side=True)
    if pos.yes > EPS:
        pos.yes_cost *= yes_left / pos.yes
        pos.yes = yes_left
    if pos.no > EPS:
        pos.no_cost *= no_left / pos.no
        pos.no = no_left
    pos.cash += yes_cash + no_cash
    return yes_cash + no_cash


def markout(fill_side: str, fill_price: float, later_mid: float, shares: float) -> float:
    """Dollar gain of a fill if valued at a later midpoint (negative: the market moved against us)."""
    if fill_side == "bid":
        return (later_mid - fill_price) * shares
    return (fill_price - later_mid) * shares
