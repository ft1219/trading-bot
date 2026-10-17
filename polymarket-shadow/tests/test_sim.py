import pytest

import rewards
import sim

YES, NO = "yes-token", "no-token"
P = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5)


def hist(mid=0.585, start=0, end=3600):
    return [(t, mid) for t in range(start, end + 1, 60)]


def trade(ts, side, price, asset=YES, size=50):
    """A taker record plus the maker order it traded with, as /v2/trades lists them with taker_only=false."""
    tx = f"0x{ts}{side}{price}"
    taker = {"timestamp": ts, "side": side, "price": price, "token_id": asset, "size": size, "transaction_hash": tx}
    maker = dict(taker, side="SELL" if side == "BUY" else "BUY")
    return [taker, maker]


def trades(*groups):
    return [r for g in groups for r in g]


def test_no_token_records_map_to_yes():
    assert sim.leg_side({"side": "BUY", "price": 0.41, "token_id": NO}, YES) == ("ask", pytest.approx(0.59))
    assert sim.leg_side({"side": "SELL", "price": 0.41, "token_id": NO}, YES) == ("bid", pytest.approx(0.59))
    assert sim.leg_side({"side": "BUY", "price": 0.41, "token_id": YES}, YES) == ("bid", 0.41)


def test_round_trip_captures_the_spread():
    pos = sim.Position()
    fills = sim.replay(pos, trades(trade(90, "SELL", 0.575), trade(400, "BUY", 0.595)), hist(), YES, P, 0)
    assert [f.side for f in fills] == ["bid", "ask"]
    assert pos.yes == pos.no == 0  # merged back into cash
    assert pos.cash == pytest.approx(20 - 20 * 0.58 - 20 * 0.41)
    assert pos.value(0.585) == pytest.approx(0.2)


def test_trade_at_our_price_does_not_fill():
    pos = sim.Position()
    assert sim.replay(pos, trades(trade(90, "SELL", 0.58), trade(95, "BUY", 0.59)), hist(), YES, P, 0) == []


def test_rounding_noise_at_our_price_does_not_fill():
    # A trade at 0.58 reported as 0.57999959 because USDC and shares are rounded to 6 decimals.
    assert sim.replay(sim.Position(), trade(90, "SELL", 0.57999959), hist(), YES, P, 0) == []


def test_no_side_trade_fills_our_bid():
    pos = sim.Position()
    fills = sim.replay(pos, trade(90, "BUY", 0.43, NO), hist(), YES, P, 0)  # = YES sold at 0.57
    assert len(fills) == 1 and fills[0].side == "bid" and fills[0].price == 0.58


def test_a_sweep_fills_an_order_behind_the_best_price():
    # Level 1 ask at 0.60. A taker buys 200 YES: 100 at 0.59, 50 at 0.60, 50 at 0.61; its average is 0.5975.
    sweep = [{"timestamp": 90, "side": "BUY", "price": 0.5975, "token_id": YES, "size": 200, "transaction_hash": "0xs"},
             {"timestamp": 90, "side": "SELL", "price": 0.59, "token_id": YES, "size": 100, "transaction_hash": "0xs"},
             {"timestamp": 90, "side": "BUY", "price": 0.40, "token_id": NO, "size": 50, "transaction_hash": "0xs"},
             {"timestamp": 90, "side": "SELL", "price": 0.61, "token_id": YES, "size": 50, "transaction_hash": "0xs"}]
    fills = sim.replay(sim.Position(), sweep, hist(), YES, P, 1)
    assert [(f.side, f.price, f.shares, f.trade_price) for f in fills] == [("ask", 0.60, 20, 0.61)]


def test_a_small_trade_fills_only_its_own_size():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=100, max_spread_c=5.5)
    pos = sim.Position()
    fills = sim.replay(pos, trades(trade(90, "SELL", 0.575, size=3), trade(100, "SELL", 0.575, size=30)),
                       hist(), YES, p, 0)
    assert [f.shares for f in fills] == [3, 17]  # the rest of the same order, not a new one
    assert pos.yes == 20


def test_budget_stops_a_second_buy_until_we_sell():
    pos = sim.Position()
    fills = sim.replay(pos, trades(trade(90, "SELL", 0.575), trade(400, "SELL", 0.575), trade(800, "BUY", 0.595)),
                       hist(), YES, P, 0)
    assert [f.side for f in fills] == ["bid", "ask"]  # second bid was not resting: no money for it


def test_selling_what_we_hold_needs_no_cash():
    pos = sim.Position(yes=20, yes_cost=11.4, cash=-11.4)
    # 11.4 held + 20 * (1 - 0.56) = 20.2 would not fit, but the ask only sells YES we already own.
    assert sim.active_sides(pos, 0.53, 0.56, P) == (False, True)


def test_requote_waits_for_the_next_minute():
    pos = sim.Position()
    p = sim.MarketParams(tick=0.01, size=10, budget_usd=100, max_spread_c=5.5)
    fills = sim.replay(pos, trades(trade(90, "SELL", 0.575), trade(100, "SELL", 0.575), trade(130, "SELL", 0.575)),
                       hist(), YES, p, 0)
    assert [f.ts for f in fills] == [90, 130]


def test_stale_midpoint_means_no_quote():
    assert sim.replay(sim.Position(), trade(1000, "SELL", 0.5), [(0, 0.585)], YES, P, 0) == []


def test_quotes_use_the_midpoint_before_the_trade():
    history = [(0, 0.585), (60, 0.585), (120, 0.40)]
    # At t=120 the midpoint jumps; a trade at t=120 still meets our old 0.58 bid.
    fills = sim.replay(sim.Position(), trade(120, "SELL", 0.40), history, YES, P, 0)
    assert len(fills) == 1 and fills[0].price == 0.58 and fills[0].mid_before == 0.585


def test_rebate_follows_the_fee_curve():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5, fee_rate=0.04, fee_exponent=1,
                         rebate_rate=0.25)
    pos = sim.Position()
    fills = sim.replay(pos, trade(90, "SELL", 0.575), hist(), YES, p, 0)
    assert fills[0].rebate == pytest.approx(0.25 * 20 * 0.04 * 0.58 * 0.42)
    assert pos.rebates == pytest.approx(fills[0].rebate)


def test_quotes_outside_the_reward_band_are_not_posted():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=1.0)
    assert sim.quotes(0.585, p, 0) == (0.58, 0.59)
    assert sim.quotes(0.585, p, 1) == (None, None)


def test_midpoint_moving_through_our_bid_fills_it_without_a_trade():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5, fee_rate=0.04, rebate_rate=0.25)
    history = [(0, 0.585), (60, 0.585), (120, 0.555), (180, 0.555)]
    pos = sim.Position()
    fills = sim.replay(pos, [], history, YES, p, 0)
    assert len(fills) == 1 and fills[0].side == "bid" and fills[0].price == 0.58 and fills[0].ts == 120
    assert fills[0].rebate == 0 and fills[0].tx == "midpoint-move"


def test_midpoint_moves_outside_the_window_are_left_for_the_other_run():
    history = [(0, 0.585), (60, 0.585), (120, 0.555)]
    assert sim.replay(sim.Position(), [], history, YES, P, 0, start=120, end=600) == []  # 120 was counted last run
    assert len(sim.replay(sim.Position(), [], history, YES, P, 0, start=60, end=120)) == 1


def test_a_trade_and_a_midpoint_move_in_the_same_minute_fill_one_order_once():
    history = [(0, 0.585), (60, 0.585), (120, 0.555), (180, 0.555)]
    p = sim.MarketParams(tick=0.01, size=10, budget_usd=100, max_spread_c=5.5)
    fills = sim.replay(sim.Position(), trade(100, "SELL", 0.56, size=4), history, YES, p, 0)
    # 4 shares by the trade, then the midpoint move takes the other 6 of the same order.
    assert [(f.ts, f.shares) for f in fills] == [(100, 4), (120, 6)]


def book(bids, asks):
    return rewards.Book(tuple(rewards.Level(px, sz) for px, sz in bids),
                        tuple(rewards.Level(px, sz) for px, sz in asks), 0.01)


def test_liquidation_walks_the_book_and_pays_the_taker_fee():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5, fee_rate=0.04, fee_exponent=1)
    pos = sim.Position(yes=20, yes_cost=11.6, no=10, no_cost=4.1, cash=-15.7)
    b = book([(0.57, 5), (0.55, 100)], [(0.60, 100)])
    fee = lambda shares, px: shares * 0.04 * px * (1 - px)
    expected = (-15.7 + 5 * 0.57 - fee(5, 0.57) + 15 * 0.55 - fee(15, 0.55) + 10 * 0.40 - fee(10, 0.40))
    assert sim.liquidation_value(pos, b, p) == pytest.approx(expected)
    assert sim.liquidation_value(pos, None, p) == pytest.approx(-15.7)  # nobody to sell to: worth nothing


def test_close_out_keeps_what_nobody_would_buy():
    pos = sim.Position(yes=20, yes_cost=11.6, cash=-11.6)
    assert sim.close_out(pos, book([(0.57, 15)], [(0.59, 100)]), P) == pytest.approx(15 * 0.57)
    assert pos.yes == 5 and pos.yes_cost == pytest.approx(11.6 * 5 / 20)


def test_markout_signs():
    assert sim.markout("bid", 0.58, 0.55, 20) == pytest.approx(-0.6)
    assert sim.markout("ask", 0.59, 0.55, 20) == pytest.approx(0.8)


def test_position_round_trips_through_json():
    pos = sim.Position(yes=3, yes_cost=1.5, cash=-1.5, fills=1, bid_quote_ts=60, bid_left=7)
    assert sim.Position.from_dict(pos.to_dict()) == pos
    old = {"yes": 1, "bid_blocked_until": 99}  # state written by the first version
    assert sim.Position.from_dict(old).yes == 1
