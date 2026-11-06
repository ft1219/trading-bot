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
        "feesEnabled": True, "feeSchedule": {"rate": 0.05, "exponent": 1}, "orderMinSize": 5, "volume24hr": 100.0,
    }
    m.update(kw)
    return m


def serial(monkeypatch):
    """Run pmapi.parallel's calls one after another (a failed call's exception is its result, as in the real one)."""
    def run(calls, workers=8):
        out = {}
        for k, fn in calls.items():
            try:
                out[k] = fn()
            except Exception as e:  # noqa: BLE001
                out[k] = e
        return out
    monkeypatch.setattr(lab.pmapi, "parallel", run)


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
    assert v["min_size"] == 5 and v["temp"] is False and v["volume_24h"] == 100.0
    assert S._sides(v) == [(0, 0.05), (1, 0.96)]
    assert lab.market_view(gamma(closed=True), NOW) is None
    assert lab.market_view(gamma(orderMinSize=None), NOW)["min_size"] == 5


def test_sides_reject_dead_markets():
    # a lone 95c ask over a 1c bid is not a 95% consensus
    assert S._sides(lab.market_view(gamma(bid=0.01, ask=0.95), NOW)) == []
    assert S.sure_thing(lab.market_view(gamma(bid=0.01, ask=0.95), NOW), random.Random(1)) is None
    assert S._sides(lab.market_view(gamma(bid=0.91, ask=0.95), NOW)) == [(0, 0.95), (1, 0.09)]


def test_sure_thing_picks_favourite_only_near_end():
    rng = random.Random(1)
    assert S.sure_thing(lab.market_view(gamma(bid=0.04, ask=0.05), NOW), rng) == (1, 0.97)
    assert S.sure_thing(lab.market_view(gamma(end_h=30, bid=0.04, ask=0.05), NOW), rng) is None
    assert S.sure_thing(lab.market_view(gamma(bid=0.5, ask=0.51), NOW), rng) is None
    temp = gamma(bid=0.04, ask=0.05, events=[{"id": "t1", "title": "Highest temperature in Paris on November 6?"}])
    assert lab.market_view(temp, NOW)["temp"] is True
    assert S.sure_thing(lab.market_view(temp, NOW), rng) is None


def test_follow_and_fade_take_opposite_sides():
    v = lab.market_view(gamma(end_h=48, bid=0.6, ask=0.61, oneDayPriceChange=0.2), NOW)
    rng = random.Random(1)
    assert S.follow_move(v, rng) == (0, 0.85)
    assert S.fade_move(v, rng) == (1, 0.85)
    # no trades behind the "move", or a temperature market: not a move
    quiet = lab.market_view(gamma(end_h=48, bid=0.6, ask=0.61, oneDayPriceChange=0.2, volume24hr=0), NOW)
    assert S.follow_move(quiet, rng) is None and S.fade_move(quiet, rng) is None
    temp = lab.market_view(gamma(end_h=48, bid=0.6, ask=0.61, oneDayPriceChange=0.2,
                                 events=[{"id": "t", "title": "Lowest temperature in Tokyo on November 7?"}]), NOW)
    assert S.follow_move(temp, rng) is None


def test_make_trade_needs_minimum_order():
    v = lab.market_view(gamma(bid=0.94, ask=0.95), NOW)
    thin = {"asks": [{"price": "0.95", "size": "3"}]}  # 3 shares < the 5-share minimum
    assert lab.make_trade("s", v, 0, 0.97, thin, NOW) is None
    deep = {"asks": [{"price": "0.95", "size": "50"}]}
    t = lab.make_trade("s", v, 0, 0.97, deep, NOW)
    assert t and t["payout_if_won"] == pytest.approx(t["legs"][0]["shares"]) and t["ends_at"] == v["ends_at"]
    assert t["legs"][0]["shares"] >= 5


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


def _gap_fetch(ask="0.30"):
    def fetch(url, body):
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": ask, "size": "100"}]} for b in body]
        raise AssertionError(url)
    return fetch


def _gap_events(ms, augmented=False):
    return {"E1": {"id": "E1", "title": "Who wins", "negRiskAugmented": augmented, "markets": ms}}


def test_price_gap_buys_complete_cheap_set_in_whole_minimum_orders():
    ms = [gamma(cid=c, bid=0.28, ask=0.30, negRisk=True, events=[{"id": "E1", "title": "Who wins"}]) for c in "xyz"]
    views = [lab.market_view(m, NOW) for m in ms]
    trades, seen = lab.price_gap_trades(views, _gap_events(ms), {"positions": [], "traded_events": {}}, NOW, _gap_fetch())
    assert len(trades) == 1 and len(trades[0]["legs"]) == 3
    t = trades[0]
    shares = t["legs"][0]["shares"]
    assert shares >= 5 and shares == int(shares)
    assert t["cost"] <= lab.GAP_BUDGET_USD and t["payout_if_won"] - t["cost"] > 0
    assert seen and seen[0]["cost_per_set"] < 1


def test_price_gap_checks_books_when_a_bid_is_missing_and_skips_augmented_yes():
    ms = [gamma(cid=c, bid=None, ask=0.30, negRisk=True, events=[{"id": "E1", "title": "Who wins"}]) for c in "xyz"]
    views = [lab.market_view(m, NOW) for m in ms]
    trades, seen = lab.price_gap_trades(views, _gap_events(ms), {"positions": [], "traded_events": {}}, NOW, _gap_fetch())
    assert len(trades) == 1  # a null bid must not hide a cheap Yes set
    trades, seen = lab.price_gap_trades(views, _gap_events(ms, augmented=True), {"positions": [], "traded_events": {}}, NOW, _gap_fetch())
    assert all(s["side"] == "no" for s in seen)  # the Yes set is never even priced
    assert trades and all(leg["outcome_index"] == 1 for leg in trades[0]["legs"])


def test_list_events_splits_crowded_slices(monkeypatch):
    serial(monkeypatch)
    crowded_from = NOW + 3600  # 2,500 events all ending inside one 10-minute window
    crowded_to = crowded_from + 600

    def fetch(url, body):
        assert "/events?" in url
        q = dict(p.split("=") for p in url.split("?")[1].split("&"))
        a = lab.parse_ts(q["end_date_min"].replace("%3A", ":"))
        b = lab.parse_ts(q["end_date_max"].replace("%3A", ":"))
        off = int(q["offset"])
        n = 2500 if (a < crowded_to and b > crowded_from) else (3 if off == 0 else 0)
        rows = []
        for i in range(max(0, min(100, n - off))):
            m = gamma(cid=f"{a}-{off}-{i}")
            del m["events"]  # nested markets do not carry their event; markets_of attaches it
            rows.append({"id": f"{a}-{off}-{i}", "title": "E", "markets": [m]})
        return rows

    events, problems = lab.list_events(NOW, fetch)
    assert len(events) > 2000
    assert problems and "not read" in problems[0]
    markets = list(lab.markets_of(events))
    assert len(markets) == len(events) and markets[0]["events"][0]["id"] == events[0]["id"]


def test_list_events_retries_one_failed_slice_and_keeps_the_rest(monkeypatch):
    serial(monkeypatch)
    calls = []

    def fetch(url, body):
        calls.append(url)
        q = dict(p.split("=") for p in url.split("?")[1].split("&"))
        if "end_date_min=" + lab.dt.datetime.fromtimestamp(NOW + 6 * 3600, lab.dt.timezone.utc).strftime("%Y-%m-%dT%H") in url \
                and len([c for c in calls if q["end_date_min"] in c]) == 1:
            raise lab.pmapi.ApiError("HTTP 502 once")  # the second slice fails the first time only
        m = gamma(cid=f"{q['end_date_min']}-{q['offset']}")
        del m["events"]
        return [{"id": f"{q['end_date_min']}", "title": "E", "markets": [m]}] if q["offset"] == "0" else []

    events, problems = lab.list_events(NOW, fetch)
    assert len(events) == 28 and problems == []  # 7 days in 6-hour slices, all read

    def always_fail(url, body):
        raise lab.pmapi.ApiError("HTTP 503")

    with pytest.raises(lab.pmapi.ApiError, match="seems down"):
        lab.list_events(NOW, always_fail)

    def one_slice_dead(url, body):
        q = dict(p.split("=") for p in url.split("?")[1].split("&"))
        if q["end_date_min"].startswith(lab.dt.datetime.fromtimestamp(NOW + 12 * 3600, lab.dt.timezone.utc).strftime("%Y-%m-%dT%H")):
            raise lab.pmapi.ApiError("HTTP 500")  # the third slice fails every time
        return fetch(url, body)

    events, problems = lab.list_events(NOW, one_slice_dead)
    assert len(events) == 27 and len(problems) == 1 and "could not be read twice" in problems[0]


def test_markets_of_marks_augmented_events():
    ev = {"id": "E", "title": "Who", "negRiskAugmented": True, "markets": [gamma(cid="a"), gamma(cid="b")]}
    assert all(m["negRiskAugmented"] is True for m in lab.markets_of([ev]))
    assert lab.market_view(next(lab.markets_of([ev])), NOW)["negRiskAugmented"] is True


def test_report_verdicts_are_judged_once_and_need_real_evidence():
    # 40 wins out of 40 at 80c: the prices alone would give that about 1 time in 7,000
    good = report.stats([{"cost": 4.0, "pnl": 1.0, "payout_if_won": 5.0, "settled_at": NOW + i * 86400} for i in range(40)])
    assert good["p_luck"] == pytest.approx(0.8 ** 40, rel=1e-3)
    assert report.verdict("sure_thing", good, 15) == "PASS"
    # 40 wins out of 40 at 95c is NOT enough: the prices alone give that 1 time in 7
    sure = report.stats([{"cost": 5, "pnl": 0.25, "payout_if_won": 5.25, "settled_at": NOW + i * 86400} for i in range(40)])
    assert report.verdict("sure_thing", sure, 15) == "FAIL"
    assert report.verdict("sure_thing", good, 5) == "too early"
    assert report.verdict("coin_flip", good, 50) == "yardstick"
    # 30 wins out of 30 at 95c is what the prices alone give 21% of the time: not a pass
    lucky = report.stats([{"cost": 4.75, "pnl": 0.25, "payout_if_won": 5.0, "settled_at": NOW + i * 86400} for i in range(30)])
    assert lucky["p_luck"] == pytest.approx(0.95 ** 30, rel=1e-3)
    assert report.verdict("sure_thing", lucky, 15) == "FAIL"
    # all on one day: no verdict yet
    one_day = report.stats([{"cost": 4.0, "pnl": 1.0, "payout_if_won": 5.0, "settled_at": NOW} for _ in range(40)])
    assert report.verdict("sure_thing", one_day, 15) == "too early"
    # a stored verdict is kept even when later numbers differ
    assert report.verdict("sure_thing", good, 15, {"verdict": "FAIL"}) == "FAIL"
    assert report.binom_tail(0, 10, 0.5) == 1.0 and report.binom_tail(10, 10, 0.5) == pytest.approx(0.5 ** 10)
    # arbitrage passes on a positive total with no losing set; a strategy that never trades is told so after a month
    arb_rows = [{"cost": 9.9, "pnl": 0.1, "payout_if_won": 10.0, "settled_at": NOW + i * 86400} for i in range(30)]
    assert report.verdict("price_gap", report.stats(arb_rows), 15) == "PASS"
    lossy = report.stats(arb_rows[:-1] + [{"cost": 9.9, "pnl": -2.4, "payout_if_won": 10.0, "settled_at": NOW + 29 * 86400}])
    assert lossy["pnl"] > 0 and report.verdict("price_gap", lossy, 15) == "FAIL"
    assert report.verdict("price_gap", report.stats([]), 29) == "nothing to judge"
    assert report.verdict("price_gap", report.stats([]), 29, opened=1) == "too early"  # a trade is open: wait for it
    assert report.verdict("price_gap", report.stats([]), 15) == "too early"


def test_no_edge_rate_is_the_mean_price_not_the_harmonic_mean():
    # half the trades at 25c, half at 85c, winning exactly what the prices predict (12 of 50 and 43 of 50):
    # that is no skill at all and must not look like it. Total cost / total payout would say the
    # no-edge rate is 0.386 and call 55 wins a 1-in-1,500 event.
    rows = [{"cost": 5.0, "payout_if_won": 20.0, "pnl": 15.0 if i < 12 else -5.0, "settled_at": NOW + i * 86400}
            for i in range(50)]
    rows += [{"cost": 5.0, "payout_if_won": 5.0 / 0.85, "pnl": (5.0 / 0.85 - 5.0) if i < 43 else -5.0,
              "settled_at": NOW + i * 86400} for i in range(50)]
    mixed = report.stats(rows)
    assert mixed["break_even_rate"] == pytest.approx(0.55, abs=1e-3)
    assert mixed["p_luck"] > 0.3
    assert report.verdict("follow_move", mixed, 15) == "FAIL"


def test_nothing_to_judge_is_not_stored_and_gives_way_to_trades(tmp_path):
    settled_dir = tmp_path / "settled"
    settled_dir.mkdir()
    state = {"positions": [], "traded_events": {}, "verdicts": {}}
    day = 86400
    t0 = lab.parse_ts(S.STRATEGIES["price_gap"]["since"] + "T00:00:00Z")  # the strategies' start date
    # a month in with nothing traded: shown, but not stored
    text, summary = report.build(tmp_path, t0 + 29 * day, state)
    assert summary["strategies"]["price_gap"]["verdict"] == "nothing to judge"
    assert state["verdicts"] == {}
    # a month in with one position still open: too early, nothing stored
    trades_dir = tmp_path / "trades"
    trades_dir.mkdir()
    lab.append_jsonl(trades_dir / "2026-12.jsonl", [{"strategy": "price_gap", "opened_at": int(t0 + 28 * day),
                                                     "event_id": "E", "cost": 9.9, "avg_price": 0.99, "title": "T",
                                                     "legs": [{"outcome": "Yes"}]}])
    state["positions"] = [{"strategy": "price_gap", "cost": 9.9}]
    text, summary = report.build(tmp_path, t0 + 29 * day, state)
    assert summary["strategies"]["price_gap"]["verdict"] == "too early" and state["verdicts"] == {}
    # later, 30 finished sets on 12 days: judged properly, and that one is stored
    rows = [{"strategy": "price_gap", "cost": 9.9, "pnl": 0.1, "payout_if_won": 10.0, "settled_at": t0 + (30 + i % 12) * day}
            for i in range(30)]
    lab.append_jsonl(settled_dir / "2026-12.jsonl", rows)
    state["positions"] = []
    text, summary = report.build(tmp_path, t0 + 48 * day, state)
    assert summary["strategies"]["price_gap"]["verdict"] == "PASS" and state["verdicts"]["price_gap"]["verdict"] == "PASS"
    # the report lists the newest buy of each strategy, so every rule's side can be seen
    assert "T at 0.990" in text


def test_full_run_with_fake_api(tmp_path, monkeypatch):
    serial(monkeypatch)
    m = gamma(cid="0xfav", end_h=5, bid=0.04, ask=0.05)

    def fetch(url, body):
        if "/markets?" in url and "closed=true" in url:
            return []
        if "/events?" in url:
            return [{"id": "ev-0xfav", "title": "E", "markets": [m]}] if "offset=0" in url else []
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": "0.95", "size": "50"}]} for b in body]
        raise AssertionError(url)

    row = lab.run(tmp_path, NOW, fetch, seed=1)
    assert row["new_trades"] >= 1 and not row["problems"]
    text = (tmp_path / "report.md").read_text()
    assert "sure_thing" in text
    assert list((tmp_path / "trades").glob("*.jsonl"))
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["traded_events"]["sure_thing"] and isinstance(state["traded_events"]["sure_thing"], dict)
    # a second run does not buy the same event again
    row2 = lab.run(tmp_path, NOW + 2400, fetch, seed=2)
    assert row2["new_trades"] == 0


def test_report_failure_is_recorded_and_leaves_a_stub_report(tmp_path, monkeypatch):
    serial(monkeypatch)
    m = gamma(cid="0xfav", end_h=5, bid=0.04, ask=0.05)

    def fetch(url, body):
        if "/markets?" in url and "closed=true" in url:
            return []
        if "/events?" in url:
            return [{"id": "ev-0xfav", "title": "E", "markets": [m]}] if "offset=0" in url else []
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": "0.95", "size": "50"}]} for b in body]
        raise AssertionError(url)

    lab.run(tmp_path, NOW, fetch, seed=1)
    good_report = (tmp_path / "report.md").read_text()
    assert "Runs in the last 24 hours: 1 (0 with a problem)" in good_report  # the current run counts

    def broken_build(*a, **k):
        raise ZeroDivisionError("report bug")

    monkeypatch.setattr(lab.report, "build", broken_build)
    with pytest.raises(ZeroDivisionError):
        lab.run(tmp_path, NOW + 2400, fetch, seed=2)
    runs = report.read_jsonl(tmp_path / "runs.jsonl")
    assert len(runs) == 2 and "report: ZeroDivisionError" in runs[-1]["problems"][-1]
    stub = (tmp_path / "report.md").read_text()
    assert stub != good_report and "could not be built" in stub and "ZeroDivisionError" in stub
    assert json.loads((tmp_path / "state.json").read_text())["positions"]  # the data itself was saved


def test_first_version_state_is_migrated_on_load(tmp_path):
    (tmp_path / "state.json").write_text(json.dumps({"traded_events": {"weather_forecast": ["111"], "sure_thing": []}}))
    st = lab.load_state(tmp_path)
    assert st["traded_events"] == {"weather_forecast": {"111": lab.FOREVER}, "sure_thing": {}}


def test_crash_is_recorded_then_raised(tmp_path, monkeypatch):
    serial(monkeypatch)

    def broken_pick(*a, **k):
        raise ConnectionResetError("boom")  # not an ApiError: a bug, not an API problem

    monkeypatch.setattr(lab, "pick_entries", broken_pick)
    with pytest.raises(ConnectionResetError):
        lab.run(tmp_path, NOW, lambda url, body: [], seed=1)
    runs = report.read_jsonl(tmp_path / "runs.jsonl")
    assert len(runs) == 1 and runs[0]["problems"] and "crash" in runs[0]["problems"][-1]
    assert (tmp_path / "state.json").exists()
