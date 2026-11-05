import json
import random

import pytest

import lab
import report
import strategies as S

NOW = 1_793_000_000.0


def gamma(cid="0xabc", end_h=10.0, bid=0.05, ask=0.06, **kw):
    m = {
        "conditionId": cid, "question": f"Q {cid}?", "active": True, "closed": False,
        "acceptingOrders": True, "enableOrderBook": True,
        "endDate": lab.dt.datetime.fromtimestamp(NOW + end_h * 3600, lab.dt.timezone.utc).isoformat(),
        "clobTokenIds": json.dumps([cid + "-yes", cid + "-no"]), "outcomes": '["Yes", "No"]',
        "bestBid": bid, "bestAsk": ask, "events": [{"id": "ev-" + cid, "title": "E"}],
        "feesEnabled": True, "feeSchedule": {"rate": 0.05, "exponent": 1},
    }
    m.update(kw)
    return m


def test_fee_curve():
    assert lab.fee(100, 0.5, 0.05) == pytest.approx(1.25)
    assert lab.fee(100, 0.95, 0.0) == 0.0


def test_fill_dollars_walks_book_and_respects_cap():
    asks = [(0.95, 2.0), (0.96, 100.0), (0.99, 100.0)]
    shares, cost = lab.fill_dollars(asks, 5.0, 0.97, 0.0)
    assert cost == pytest.approx(5.0)
    assert shares == pytest.approx(2 + (5 - 1.9) / 0.96)
    shares, cost = lab.fill_dollars([(0.98, 100.0)], 5.0, 0.97, 0.0)
    assert shares == 0 and cost == 0


def test_fill_shares_needs_depth():
    assert lab.fill_shares([(0.3, 1.0), (0.4, 1.0)], 2.0, 0.0) == pytest.approx(0.7)
    assert lab.fill_shares([(0.3, 1.0)], 2.0, 0.0) is None


def test_market_view_and_sides():
    v = lab.market_view(gamma(bid=0.04, ask=0.05), NOW)
    assert v["hours_left"] == pytest.approx(10)
    assert S._sides(v) == [(0, 0.05), (1, 0.96)]
    assert lab.market_view(gamma(closed=True), NOW) is None


def test_sure_thing_picks_favourite_only_near_end():
    rng = random.Random(1)
    assert S.sure_thing(lab.market_view(gamma(bid=0.04, ask=0.05), NOW), rng) == (1, 0.97)
    assert S.sure_thing(lab.market_view(gamma(end_h=30, bid=0.04, ask=0.05), NOW), rng) is None
    assert S.sure_thing(lab.market_view(gamma(bid=0.5, ask=0.51), NOW), rng) is None


def test_follow_and_fade_take_opposite_sides():
    v = lab.market_view(gamma(end_h=48, bid=0.6, ask=0.61, oneDayPriceChange=0.2), NOW)
    rng = random.Random(1)
    assert S.follow_move(v, rng) == (0, 0.85)
    assert S.fade_move(v, rng) == (1, 0.85)


def test_settle_pays_winners_and_keeps_open():
    state = {"positions": [
        {"strategy": "s", "cost": 4.8, "legs": [{"condition_id": "a", "outcome_index": 1, "shares": 5.0}]},
        {"strategy": "s", "cost": 4.8, "legs": [{"condition_id": "b", "outcome_index": 0, "shares": 5.0}]},
        {"strategy": "s", "cost": 1.0, "legs": [{"condition_id": "c", "outcome_index": 0, "shares": 5.0}]},
    ], "traded_events": {}}

    def fetch(url, body):
        return [{"conditionId": "a", "closed": True, "outcomePrices": '["0", "1"]'},
                {"conditionId": "b", "closed": True, "outcomePrices": '["0", "1"]'}]

    done = lab.settle(state, NOW, fetch)
    assert [d["pnl"] for d in done] == [pytest.approx(0.2), pytest.approx(-4.8)]
    assert len(state["positions"]) == 1


def test_final_prices_rejects_unsettled():
    assert lab.final_prices({"closed": True, "outcomePrices": '["0.97", "0.03"]'}) is None
    assert lab.final_prices({"closed": False, "outcomePrices": '["1", "0"]'}) is None
    assert lab.final_prices({"closed": True, "outcomePrices": '["0.5", "0.5"]'}) == [0.5, 0.5]


def test_price_gap_buys_complete_cheap_set():
    ms = [gamma(cid=c, bid=0.28, ask=0.30, negRisk=True, events=[{"id": "E1", "title": "Who wins"}]) for c in "xyz"]
    views = [lab.market_view(m, NOW) for m in ms]

    def fetch(url, body):
        if "/events" in url:
            return [{"title": "Who wins", "markets": ms}]
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": "0.30", "size": "100"}]} for b in body]
        raise AssertionError(url)

    trades, seen = lab.price_gap_trades(views, {"positions": [], "traded_events": {}}, NOW, fetch)
    assert len(trades) == 1 and len(trades[0]["legs"]) == 3
    t = trades[0]
    shares = t["legs"][0]["shares"]
    assert t["cost"] <= lab.GAP_BUDGET_USD and shares - t["cost"] > 0
    assert seen and seen[0]["cost_per_set"] < 1


def test_report_verdicts():
    st = report.stats([{"cost": 5, "pnl": 0.3}] * 40)
    assert report.verdict("x", st, 15, -0.02) == "PASS"
    assert report.verdict("x", st, 5, -0.02) == "too early"
    bad = report.stats([{"cost": 5, "pnl": 0.3}] * 30 + [{"cost": 5, "pnl": -5}] * 10)
    assert report.verdict("x", bad, 15, None) == "FAIL"


def test_full_run_with_fake_api(tmp_path):
    m = gamma(cid="0xfav", end_h=5, bid=0.04, ask=0.05)

    def fetch(url, body):
        if "/markets?" in url and "closed=true" in url:
            return []
        if "/markets?" in url:
            return [m] if "offset=0" in url else []
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": "0.95", "size": "50"}]} for b in body]
        if "/events" in url:
            return []
        raise AssertionError(url)

    row = lab.run(tmp_path, NOW, fetch, seed=1)
    assert row["new_trades"] >= 1
    text = (tmp_path / "report.md").read_text()
    assert "sure_thing" in text
    # a second run does not buy the same event again
    row2 = lab.run(tmp_path, NOW + 2400, fetch, seed=2)
    assert row2["new_trades"] == 0
