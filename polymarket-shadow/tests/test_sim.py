import pytest

import sim

YES, NO = "yes-token", "no-token"
P = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5)


def hist(mid=0.585, start=0, end=3600):
    return [(t, mid) for t in range(start, end + 1, 60)]


def trade(ts, side, price, asset=YES):
    return {"timestamp": ts, "side": side, "price": price, "asset": asset, "size": 50, "transactionHash": f"0x{ts}"}


def test_no_token_trades_map_to_yes():
    assert sim.yes_equivalent(trade(1, "BUY", 0.41, NO), YES) == ("SELL", pytest.approx(0.59))
    assert sim.yes_equivalent(trade(1, "SELL", 0.41, NO), YES) == ("BUY", pytest.approx(0.59))


def test_round_trip_captures_the_spread():
    pos = sim.Position()
    fills = sim.replay(pos, [trade(90, "SELL", 0.575), trade(400, "BUY", 0.595)], hist(), YES, P, 0)
    assert [f.side for f in fills] == ["bid", "ask"]
    assert pos.yes == pos.no == 0  # merged back into cash
    assert pos.cash == pytest.approx(20 - 20 * 0.58 - 20 * 0.41)
    assert pos.value(0.585) == pytest.approx(0.2)


def test_trade_at_our_price_does_not_fill():
    pos = sim.Position()
    assert sim.replay(pos, [trade(90, "SELL", 0.58), trade(95, "BUY", 0.59)], hist(), YES, P, 0) == []


def test_no_side_trade_fills_our_bid():
    pos = sim.Position()
    fills = sim.replay(pos, [trade(90, "BUY", 0.43, NO)], hist(), YES, P, 0)  # = YES sold at 0.57
    assert len(fills) == 1 and fills[0].side == "bid" and fills[0].price == 0.58


def test_budget_stops_a_second_buy_until_we_sell():
    pos = sim.Position()
    trades = [trade(90, "SELL", 0.575), trade(400, "SELL", 0.575), trade(800, "BUY", 0.595)]
    fills = sim.replay(pos, trades, hist(), YES, P, 0)
    assert [f.side for f in fills] == ["bid", "ask"]  # second bid was not resting: no money for it


def test_requote_waits_for_the_next_minute():
    pos = sim.Position()
    p = sim.MarketParams(tick=0.01, size=10, budget_usd=100, max_spread_c=5.5)
    fills = sim.replay(pos, [trade(90, "SELL", 0.575), trade(100, "SELL", 0.575), trade(130, "SELL", 0.575)],
                       hist(), YES, p, 0)
    assert [f.ts for f in fills] == [90, 130]


def test_stale_midpoint_means_no_quote():
    pos = sim.Position()
    assert sim.replay(pos, [trade(1000, "SELL", 0.5)], [(0, 0.585)], YES, P, 0) == []


def test_quotes_use_the_midpoint_before_the_trade():
    pos = sim.Position()
    history = [(0, 0.585), (60, 0.585), (120, 0.40)]
    # At t=120 the midpoint jumps; a trade at t=120 still meets our old 0.58 bid.
    fills = sim.replay(pos, [trade(120, "SELL", 0.40)], history, YES, P, 0)
    assert len(fills) == 1 and fills[0].price == 0.58 and fills[0].mid_before == 0.585


def test_rebate_follows_the_fee_curve():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=5.5, fee_rate=0.04, fee_exponent=1, rebate_rate=0.25)
    pos = sim.Position()
    fills = sim.replay(pos, [trade(90, "SELL", 0.575)], hist(), YES, p, 0)
    assert fills[0].rebate == pytest.approx(0.25 * 20 * 0.04 * 0.58 * 0.42)
    assert pos.rebates == pytest.approx(fills[0].rebate)


def test_quotes_outside_the_reward_band_are_not_posted():
    p = sim.MarketParams(tick=0.01, size=20, budget_usd=20, max_spread_c=1.0)
    assert sim.quotes(0.585, p, 0) == (0.58, 0.59)
    assert sim.quotes(0.585, p, 1) == (None, None)


def test_close_out_and_markout():
    pos = sim.Position(yes=20, yes_cost=11.6, cash=-11.6)
    assert sim.close_out(pos, 0.57, 0.59) == pytest.approx(11.4)
    assert pos.value(0.5) == pytest.approx(-0.2)
    assert sim.markout("bid", 0.58, 0.55, 20) == pytest.approx(-0.6)
    assert sim.markout("ask", 0.59, 0.55, 20) == pytest.approx(0.8)


def test_position_round_trips_through_json():
    pos = sim.Position(yes=3, yes_cost=1.5, cash=-1.5, fills=1)
    assert sim.Position.from_dict(pos.to_dict()) == pos
