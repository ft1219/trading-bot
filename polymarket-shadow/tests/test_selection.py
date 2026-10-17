import datetime as dt

import selection

NOW = dt.datetime(2026, 10, 17, 4, 0, tzinfo=dt.timezone.utc)
S = selection.Settings()


def market(cid="0xabc", price=0.585, end="2026-12-01T00:00:00Z", **over):
    m = {"condition_id": cid, "question": "Q?", "active": True, "closed": False, "accepting_orders": True,
         "enable_order_book": True, "game_start_time": None, "seconds_delay": 0, "end_date_iso": end,
         "minimum_tick_size": 0.01, "minimum_order_size": 5, "neg_risk": False,
         "tokens": [{"token_id": f"{cid}-y", "outcome": "Yes", "price": price},
                    {"token_id": f"{cid}-n", "outcome": "No", "price": 1 - price}]}
    m.update(over)
    return m


def config(rate=500, min_size=20, spread=5.5):
    return {"total_daily_rate": rate, "rewards_min_size": min_size, "rewards_max_spread": spread}


def test_prefilter_keeps_a_good_market_and_drops_bad_ones():
    markets = [market("0xgood"), market("0xsoon", end="2026-10-20T00:00:00Z"), market("0xedge", price=0.95),
               market("0xgame", game_start_time="2026-10-17T18:00:00Z"), market("0xclosed", closed=True),
               market("0xbig"), market("0xpoor"), market("0xnocfg")]
    configs = {m["condition_id"]: config() for m in markets}
    configs["0xbig"] = config(min_size=200)
    configs["0xpoor"] = config(rate=3)
    del configs["0xnocfg"]
    out = selection.prefilter(markets, configs, NOW, S)
    assert [c.condition_id for c in out] == ["0xgood"]
    assert out[0].yes_token == "0xgood-y" and out[0].no_token == "0xgood-n"


def test_order_size_fits_the_budget():
    c = selection.prefilter([market()], {"0xabc": config()}, NOW, S)[0]
    assert selection.order_size(c, 0.58, 0.59, 20) == 20
    assert selection.order_size(c, 0.58, 0.59, 15) == 0  # cannot reach the 20-share minimum


def test_scoring_and_choice_use_the_live_book(fx):
    c = selection.prefilter([market()], {"0xabc": config()}, NOW, S)[0]
    scored = selection.score_candidates([c], {"0xabc-y": fx("book_yes")}, S)
    assert len(scored) == 1
    assert 0 < scored[0].expected_low <= scored[0].expected_high < 500
    chosen = selection.choose(scored, S)
    assert chosen[0].pilot and chosen[0].rank == 1


def test_fee_schedule_from_gamma(fx):
    c = selection.prefilter([market()], {"0xabc": config()}, NOW, S)[0]
    selection.apply_fees(c, fx("gamma_market"))
    assert (c.fee_rate, c.fee_exponent, c.rebate_rate) == (0.04, 1.0, 0.25)
    d = selection.prefilter([market()], {"0xabc": config()}, NOW, S)[0]
    selection.apply_fees(d, fx("gamma_market_no_fees"))
    assert d.fee_rate == 0 and d.rebate_rate == 0
