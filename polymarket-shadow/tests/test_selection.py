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
               market("0xbig"), market("0xpoor"), market("0xnocfg"), market("0xnomin")]
    configs = {m["condition_id"]: config() for m in markets}
    configs["0xbig"] = config(min_size=200)
    configs["0xnomin"] = config(min_size=None)
    configs["0xpoor"] = config(rate=3)
    del configs["0xnocfg"]
    out = selection.prefilter(markets, configs, NOW, S)
    assert [c.condition_id for c in out] == ["0xgood"]
    assert out[0].yes_token == "0xgood-y" and out[0].no_token == "0xgood-n"


def test_order_size_fits_the_budget():
    c = selection.prefilter([market()], {"0xabc": config()}, NOW, S)[0]
    assert selection.order_size(c, 20) == 20
    assert selection.order_size(c, 15) == 0  # cannot reach the 20-share minimum
    # Sized for the dearest pair (closest prices, midpoint between ticks), so both sides always fit.
    assert selection.order_size(c, 25) == 25


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


def _cand(cid, low, high, thin):
    return selection.Candidate(condition_id=cid, question="", yes_token="y", no_token="n", end_date=None,
                               neg_risk=False, tick=0.01, order_min=5, min_size=20, max_spread_c=4.5,
                               daily_rate=50, expected_low=low, expected_high=high, thin=thin)


def test_pilots_come_only_from_markets_others_already_quote():
    scored = [_cand(f"0xe{i}", 10 - i, 10 - i, False) for i in range(3)] + \
             [_cand(f"0xt{i}", 0, 50 - i, True) for i in range(8)]
    s = selection.Settings(watch_markets=6, pilot_markets=2, thin_markets=2)
    chosen = selection.choose(scored, s)
    # Only 3 established markets, so thin ones fill the rest of the 6 slots.
    assert [c.condition_id for c in chosen] == ["0xe0", "0xe1", "0xe2", "0xt0", "0xt1", "0xt2"]
    assert [c.condition_id for c in chosen if c.pilot] == ["0xe0", "0xe1"]
    many = [_cand(f"0xe{i}", 10 - i, 10 - i, False) for i in range(9)] + scored[3:]
    chosen = selection.choose(many, s)
    assert sum(c.thin for c in chosen) == 2 and len(chosen) == 6  # thin slots are capped when there is a choice
    only_thin = selection.choose([_cand("0xt", 0, 50, True)], s)
    assert len(only_thin) == 1 and not only_thin[0].pilot


def test_a_thin_book_scores_no_cautious_reward():
    c = selection.prefilter([market()], {"0xabc": config(rate=60, spread=4.5)}, NOW, S)[0]
    raw = {"bids": [{"price": "0.31", "size": "51"}], "asks": [{"price": "0.89", "size": "66"}], "tick_size": "0.01"}
    scored = selection.score_candidates([c], {"0xabc-y": raw}, selection.Settings(min_mid=0.1, max_mid=0.9))
    assert scored and scored[0].thin and scored[0].expected_low == 0 and scored[0].expected_high == 60


def test_thin_markets_never_take_the_pilot_slots():
    s = selection.Settings(watch_markets=3, pilot_markets=2, thin_markets=5)
    scored = [_cand("0xe1", 5, 9, False), _cand("0xe2", 4, 8, False), _cand("0xe3", 3, 7, False)] + \
             [_cand(f"0xt{i}", 0, 20, True) for i in range(5)]
    chosen = selection.choose(scored, s)
    assert [c.condition_id for c in chosen if c.pilot] == ["0xe1", "0xe2"]
    assert len(chosen) == 3
