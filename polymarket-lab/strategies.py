"""
The strategies the lab tests side by side, with pretend money only.

Every rule here is fixed before the test starts, so a strategy cannot be
tuned to the results it is being judged on. To try a new idea, add a new
strategy with a new name; to drop one, set "active": False (its record
stays in the report). Changing an existing strategy's rule means giving it a
new name, so the old results are never mixed with the new rule.

Every strategy is a buyer that pays the real asking price in the live order
book (plus Polymarket's taker fee), then holds to the result. Taking the
asking price is something a real small trader can always do, so these
pretend trades are close to what real ones would have been. The old
practice mode tested resting orders instead, which paper trading cannot
judge well.

A market here is a Gamma market dict plus a few derived fields added by
lab.market_view(): "hours_left" (to its end date), "hours_to_start" (to
the game start, sports only), "sport" (Gamma's sportsMarketType or None),
"tokens", "outcomes".
"""
from __future__ import annotations

import random
from typing import Callable

STAKE_USD = 5.0  # pretend dollars per trade
MAX_NEW_PER_RUN = 8  # per strategy, so one busy hour cannot swamp the record

SPORT_LINES = ("moneyline", "totals", "spreads")


def _sides(m: dict):
    """(index, best ask) for both outcomes, from Gamma's quote of outcome 0."""
    bid, ask = m.get("bestBid"), m.get("bestAsk")
    if bid is None or ask is None:
        return []
    bid, ask = float(bid), float(ask)
    if not (0 < bid <= ask < 1):
        return []
    return [(0, ask), (1, round(1 - bid, 6))]


def sure_thing(m: dict, rng: random.Random):
    """Idea 1: buy the near-certain side (90-97 cents) in the last 24 hours."""
    if not (0 < m["hours_left"] <= 24):
        return None
    if m["sport"] and m.get("hours_to_start") is not None and m["hours_to_start"] < 0:
        return None  # game already running: prices move by the minute
    for i, ask in _sides(m):
        if 0.90 <= ask <= 0.97:
            return i, 0.97
    return None


def safe_no_week(m: dict, rng: random.Random):
    """Longer version of idea 1, non-sports: favourite at 92-98.5 cents, 1-7 days left."""
    if m["sport"] or not (24 < m["hours_left"] <= 168):
        return None
    for i, ask in _sides(m):
        if 0.92 <= ask <= 0.985:
            return i, 0.985
    return None


def sports_underdog(m: dict, rng: random.Random):
    """
    From the history check: cheap sides of sports lines (15-35 cents) won more
    often than their price in the old data. That may be a data trap (busy,
    surprising games are over-represented), so it is tested here with real
    prices, in the 3 hours before the game.
    """
    if m["sport"] not in SPORT_LINES:
        return None
    h = m.get("hours_to_start")
    if h is None or not (0 < h <= 3):
        return None
    for i, ask in _sides(m):
        if 0.15 <= ask <= 0.35:
            return i, 0.35
    return None


def follow_move(m: dict, rng: random.Random):
    """Non-sports, ends within 7 days, moved 10+ cents in a day: buy the side that rose."""
    ch = m.get("oneDayPriceChange")
    if m["sport"] or ch is None or abs(float(ch)) < 0.10 or not (6 < m["hours_left"] <= 168):
        return None
    i = 0 if float(ch) > 0 else 1
    for j, ask in _sides(m):
        if j == i and 0.10 <= ask <= 0.85:
            return i, 0.85
    return None


def fade_move(m: dict, rng: random.Random):
    """Same moves as follow_move, but buy the side that fell (bet on an overreaction)."""
    ch = m.get("oneDayPriceChange")
    if m["sport"] or ch is None or abs(float(ch)) < 0.10 or not (6 < m["hours_left"] <= 168):
        return None
    i = 1 if float(ch) > 0 else 0
    for j, ask in _sides(m):
        if j == i and 0.10 <= ask <= 0.85:
            return i, 0.85
    return None


def coin_flip(m: dict, rng: random.Random):
    """
    Yardstick, not a strategy: a random side of a random market ending within
    3 days, priced 20-80 cents. It should lose a little (the price gap and
    fees). A real strategy has to beat it clearly, not just get lucky.
    """
    if not (1 < m["hours_left"] <= 72) or rng.random() > 0.02:
        return None
    sides = [(i, a) for i, a in _sides(m) if 0.20 <= a <= 0.80]
    if not sides:
        return None
    i, ask = rng.choice(sides)
    return i, min(0.80, ask + 0.01)


Rule = Callable[[dict, random.Random], "tuple[int, float] | None"]

# name -> settings. "plain" is what the phone report shows.
STRATEGIES: dict[str, dict] = {
    "sure_thing": {"rule": sure_thing, "active": True, "since": "2026-11-05",
                   "plain": "Buy the almost-sure side (90-97c) in the last 24 hours"},
    "safe_no_week": {"rule": safe_no_week, "active": True, "since": "2026-11-05",
                     "plain": "Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports"},
    "sports_underdog": {"rule": sports_underdog, "active": True, "since": "2026-11-05",
                        "plain": "Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off"},
    "follow_move": {"rule": follow_move, "active": True, "since": "2026-11-05",
                    "plain": "After a 10c+ jump in a day, buy the side that went up"},
    "fade_move": {"rule": fade_move, "active": True, "since": "2026-11-05",
                  "plain": "After a 10c+ jump in a day, buy the side that went down"},
    "weather_forecast": {"rule": None, "active": True, "since": "2026-11-05",
                         "plain": "Daily temperature markets: buy where two weather-model ensembles say the price is 10c+ too low"},
    "price_gap": {"rule": None, "active": True, "since": "2026-11-05",
                  "plain": "Multi-choice markets whose prices add up to less than $1: buy every choice"},
    "coin_flip": {"rule": coin_flip, "active": True, "since": "2026-11-05",
                  "plain": "Yardstick: random side, random market (should lose a little)"},
}
