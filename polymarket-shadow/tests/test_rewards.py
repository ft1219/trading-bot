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


def test_thin_when_either_side_lacks_depth_in_the_band():
    full = book([(0.58, 30), (0.40, 500)], [(0.59, 30)])
    assert not rewards.is_thin(full, 0.585, 5.5, 20)
    empty_near_mid = book([(0.31, 50)], [(0.89, 60)])  # 58-cent gap: nobody inside a 4.5-cent band
    assert rewards.is_thin(empty_near_mid, 0.60, 4.5, 20)
    one_side = book([(0.58, 30)], [(0.59, 5), (0.70, 500)])
    assert rewards.is_thin(one_side, 0.585, 5.5, 20)


def test_makers_in_the_band_are_moved_up_to_our_price_for_the_high_bound():
    b = book([(0.55, 100)], [(0.62, 100)])  # 3.5 cents out each side, band 5.5 cents
    plain = rewards.competition(b, 0.585, 5.5, 20)
    matched = rewards.competition(b, 0.585, 5.5, 20, bid_c=0.5, ask_c=0.5)
    assert matched.high > plain.high
    assert matched.low == plain.low  # the optimistic bound stays on the real book
    s = rewards.order_score(5.5, 0.5)
    assert matched.high == pytest.approx((100 * s + 100 * s + 100 * s) / 3)
    # Makers already closer than us keep their own (better) score; makers outside the band stay out.
    close = book([(0.584, 100)], [(0.70, 100)])
    m = rewards.competition(close, 0.585, 5.5, 20, bid_c=1.5, ask_c=1.5)
    assert m.high == pytest.approx(100 * rewards.order_score(5.5, 0.1) / 3)


def test_makers_exactly_at_the_band_edge_are_outside_it():
    # 0.315 - 0.28 and 0.35 - 0.315 are 3.5 cents, which floats compute as a hair under 3.5.
    edge = book([(0.28, 500)], [(0.35, 500)])
    assert rewards.depth_in_band(edge.bids, 0.315, 3.5) == 0
    assert rewards.is_thin(edge, 0.315, 3.5, 20)
    assert rewards.score_quotes(edge, 0.30, 0.33, 20, 3.5, 20).thin


def test_an_unknown_minimum_size_still_finds_an_empty_band_thin():
    assert rewards.is_thin(book([(0.31, 500)], [(0.89, 500)]), 0.60, 4.5, 0)
