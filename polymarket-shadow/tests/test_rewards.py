import pytest

import rewards
from rewards import Book, Level


def book(bids, asks, tick=0.01):
    return Book(tuple(Level(p, s) for p, s in bids), tuple(Level(p, s) for p, s in asks), tick)


def test_order_score_matches_docs_formula():
    assert rewards.order_score(3, 1) == pytest.approx((2 / 3) ** 2)
    assert rewards.order_score(3, 0) == 1
    assert rewards.order_score(3, 3) == 0  # at the max spread: nothing
    assert rewards.order_score(3, 7) == 0  # far outside: nothing (the raw formula would go positive)


def test_docs_worked_example_side_one():
    # Docs: adjusted mid 0.50, v = 3c; 100 bid at 0.49 and 200 bid at 0.48 on YES,
    # plus 100 ask on NO at 0.51 (= a YES bid at 0.49). Q_one = 111.11.
    b = book([(0.49, 200), (0.48, 200)], [])
    assert rewards.side_score(b.bids, 0.50, 3) == pytest.approx(111.111, abs=1e-3)


def test_q_min_single_sided_rules():
    assert rewards.q_min(90, 30, 0.5) == 30
    assert rewards.q_min(90, 0, 0.5) == 30  # one side only: divided by 3
    assert rewards.q_min(90, 0, 0.95) == 0  # outside 0.10-0.90 both sides are needed
    assert rewards.q_min(90, 60, 0.05) == 60


def test_parse_live_book(fx):
    b = rewards.parse_book(fx("book_yes"))
    assert b.best_bid == 0.58 and b.best_ask == 0.59
    assert b.tick == 0.01
    assert all(b.bids[i].price > b.bids[i + 1].price for i in range(len(b.bids) - 1))
    assert all(b.asks[i].price < b.asks[i + 1].price for i in range(len(b.asks) - 1))


def test_yes_and_no_books_mirror(fx):
    yes, no = rewards.parse_book(fx("book_yes")), rewards.parse_book(fx("book_no"))
    assert [(round(1 - l.price, 2), l.size) for l in yes.asks] == [(l.price, l.size) for l in no.bids]


def test_adjusted_midpoint_skips_dust():
    b = book([(0.50, 5), (0.49, 100)], [(0.52, 100)])
    assert rewards.adjusted_midpoint(b, 20) == pytest.approx(0.505)
    assert rewards.adjusted_midpoint(b, 1) == pytest.approx(0.51)
    assert rewards.adjusted_midpoint(book([], [(0.5, 10)]), 1) is None


def test_quote_prices_on_and_between_ticks():
    assert rewards.quote_prices(0.585, 0.01, 0) == (0.58, 0.59)
    assert rewards.quote_prices(0.585, 0.01, 1) == (0.57, 0.60)
    assert rewards.quote_prices(0.58, 0.01, 0) == (0.57, 0.59)  # never quote at the midpoint itself
    assert rewards.quote_prices(0.5855, 0.001, 0) == (0.585, 0.586)


def test_competition_bounds_and_our_share():
    b = book([(0.58, 1000), (0.57, 10)], [(0.59, 500)])
    comp = rewards.competition(b, 0.585, 5.5, 20)
    assert 0 < comp.low <= comp.high
    ours = rewards.our_score(0.57, 0.60, 20, 0.585, 5.5, 20, comp)
    assert 0 < ours.share_low <= ours.share_high < 1
    assert ours.q_min == pytest.approx(min(ours.q_one, ours.q_two))  # balanced two-sided


def test_one_sided_and_undersized_quotes():
    comp = rewards.Competition(10, 30)
    one = rewards.our_score(0.57, None, 20, 0.585, 5.5, 20, comp)
    assert one.q_min == pytest.approx(one.q_one / 3)
    assert rewards.our_score(0.57, 0.60, 19, 0.585, 5.5, 20, comp).q_min == 0
