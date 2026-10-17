import json

import pmapi
import snapshot
from selection import Settings

CID = "0xb0ea6c2f159bac649d481edc3d471fd8b9a912793ce16585e2a2333ad98821c3"
T_START = 1792190000  # inside the fixture's price history and trades
T_END = 1792209018    # when the fixture book was taken


class FakeApi:
    """Serves the recorded live responses in tests/fixtures."""

    def __init__(self, fx, fail_trades=False, cut_short=False):
        self.fx = fx
        self.fail_trades = fail_trades
        self.cut_short = cut_short
        m = fx("clob_market")
        m.update({"active": True, "closed": False, "accepting_orders": True, "enable_order_book": True})
        self.market = m
        self.yes = next(t["token_id"] for t in m["tokens"] if t["outcome"] == "Yes")
        self.no = next(t["token_id"] for t in m["tokens"] if t["outcome"] == "No")

    parallel = staticmethod(pmapi.parallel)

    def sampling_markets(self):
        return [self.market]

    def current_reward_configs(self):
        return {CID: {"condition_id": CID, "total_daily_rate": 500, "rewards_min_size": 20, "rewards_max_spread": 5.5}}

    def books(self, tokens):
        return {t: (self.fx("book_yes") if t == self.yes else self.fx("book_no")) for t in tokens}

    def gamma_markets(self, cids):
        return {CID: self.fx("gamma_market")}

    def price_history(self, token, start, end):
        return [(int(p["t"]), float(p["p"])) for p in self.fx("history")["history"] if start <= p["t"] <= end]

    def trades_since(self, cid, since):
        if self.fail_trades:
            raise pmapi.ApiError("boom")
        trades = [t for t in self.fx("trades_all") if t["timestamp"] > since]
        return sorted(trades, key=lambda t: t["timestamp"]), not self.cut_short


def test_two_runs_record_samples_fills_and_a_report(tmp_path, fx):
    api = FakeApi(fx)
    s = Settings(pilot_markets=1)
    log1 = snapshot.run(tmp_path, now=T_START, api=api, s=s)
    # The run that picks the watchlist takes no reward sample from the same books.
    assert log1["errors"] == [] and log1["markets"] == 1 and log1["samples"] == 0
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["watchlist_day"] == snapshot.utc_day(T_START)
    assert state["markets"][CID]["info"]["fee_rate"] == 0.04

    log2 = snapshot.run(tmp_path, now=T_START + 2400, api=api, s=s)
    assert log2["errors"] == [] and log2["samples"] == 1
    log3 = snapshot.run(tmp_path, now=T_END, api=api, s=s)  # the next UTC day: a new watchlist, so no sample
    assert log3["errors"] == [] and log3["samples"] == 0
    samples = [json.loads(line) for d in sorted((tmp_path / "days").iterdir()) if (d / "samples.jsonl").exists()
               for line in (d / "samples.jsonl").read_text().splitlines()]
    assert len(samples) == 1 and samples[0]["dt"] == 2400
    for lv in samples[0]["levels"].values():
        assert 0 <= lv["share_low"] <= lv["share_high"] <= 1
        assert lv["reward_mid"] is not None and not lv["thin"]
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["trades_until"] == T_END - snapshot.TRADE_SETTLE_S
    replayed = [t for t in fx("trades_all") if T_START - 120 < t["timestamp"] <= T_END - 120]
    assert replayed, "fixture should contain trades in the replay window"
    report = (tmp_path / "report.md").read_text()
    assert "Gate A" in report and "NOT ENOUGH DATA YET" in report


def test_failed_trade_fetch_leaves_the_window_for_next_run(tmp_path, fx):
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=FakeApi(fx, fail_trades=True), s=Settings())
    assert any("boom" in e for e in log["errors"])
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["trades_until"] == T_START - snapshot.TRADE_SETTLE_S


def test_a_market_leaving_the_list_is_sold_at_the_touch(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings())
    state = json.loads((tmp_path / "state.json").read_text())
    state["markets"][CID]["positions"]["0"].update({"yes": 20, "yes_cost": 11.6, "cash": -11.6})
    state["markets"][CID]["trades_until"] = T_START + 86400 - snapshot.TRADE_SETTLE_S  # nothing left to replay
    (tmp_path / "state.json").write_text(json.dumps(state))
    api.market["accepting_orders"] = False  # gone from tomorrow's list
    snapshot.run(tmp_path, now=T_START + 86400, api=api, s=Settings())
    day = snapshot.utc_day(T_START + 86400)
    rows = [json.loads(line) for line in (tmp_path / "days" / day / "closeouts.jsonl").read_text().splitlines()]
    row0 = next(r for r in rows if r["level"] == 0)
    assert row0["received"] == round(20 * 0.58 - 20 * 0.04 * 0.58 * 0.42, 6)  # best bid, less the taker fee
    assert CID not in json.loads((tmp_path / "state.json").read_text())["markets"]


def test_markouts_are_written_after_the_horizon(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings())
    state = json.loads((tmp_path / "state.json").read_text())
    state["pending_markouts"] = [{"condition_id": CID, "yes_token": api.yes, "pilot": True, "level": 1,
                                  "ts": T_START, "target": T_START + 3600, "horizon": 3600,
                                  "side": "bid", "price": 0.55, "shares": 20}]
    (tmp_path / "state.json").write_text(json.dumps(state))
    snapshot.run(tmp_path, now=T_START + 7200, api=api, s=Settings())
    day = snapshot.utc_day(T_START + 7200)
    rows = [json.loads(line) for line in (tmp_path / "days" / day / "markouts.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["fill_ts"] == T_START and r["price"] == 0.55]
    assert len(rows) == 1 and rows[0]["horizon"] == 3600
    assert rows[0]["markout_usd"] == round((rows[0]["later_mid"] - 0.55) * 20, 6)


class ThinBookApi(FakeApi):
    """Same market, but nobody else quotes within the reward band."""

    def books(self, tokens):
        thin = {"bids": [{"price": "0.40", "size": "500"}], "asks": [{"price": "0.77", "size": "500"}],
                "tick_size": "0.01", "asset_id": self.yes}
        return {t: thin for t in tokens}


def test_a_thin_market_is_watched_but_never_the_pilot(tmp_path, fx):
    snapshot.run(tmp_path, now=T_START, api=ThinBookApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=ThinBookApi(fx), s=Settings())
    assert log["errors"] == [] and log["samples"] == 1
    state = json.loads((tmp_path / "state.json").read_text())
    info = state["markets"][CID]["info"]
    assert info["thin"] and not info["pilot"] and info["expected_low"] == 0
    sample = json.loads((tmp_path / "days" / snapshot.utc_day(T_START) / "samples.jsonl").read_text())
    assert sample["thin"]
    for lv in sample["levels"].values():
        assert lv["est_low"] == 0 and lv["est_high"] > 0


def test_positions_are_valued_at_the_touch(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings())
    state = json.loads((tmp_path / "state.json").read_text())
    state["markets"][CID]["positions"]["1"].update({"yes": 20, "yes_cost": 11.6, "cash": -11.6})
    state["markets"][CID]["trades_until"] = T_START + 3000  # nothing to replay
    (tmp_path / "state.json").write_text(json.dumps(state))
    snapshot.run(tmp_path, now=T_START + 3000, api=api, s=Settings())
    rows = [json.loads(line) for line in
            (tmp_path / "days" / snapshot.utc_day(T_START) / "samples.jsonl").read_text().splitlines()]
    lv = rows[-1]["levels"]["1"]
    assert lv["value"] == round(-11.6 + 20 * 0.58 - 20 * 0.04 * 0.58 * 0.42, 6)  # sold at the bid, after the fee
    assert lv["value_mid"] > lv["value"]


def test_a_cut_short_trade_history_keeps_the_day_out_of_the_check(tmp_path, fx):
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings(pilot_markets=1))
    log = snapshot.run(tmp_path, now=T_START + 2400, api=FakeApi(fx, cut_short=True), s=Settings(pilot_markets=1))
    assert any("cut short" in e for e in log["errors"])
    gaps = (tmp_path / "days" / snapshot.utc_day(T_START) / "gaps.jsonl").read_text().splitlines()
    assert len(gaps) == 1 and json.loads(gaps[0])["pilot"]
    import report
    rows = report.daily_rows(tmp_path, 1, T_START + 2400)
    assert not rows[-1]["levels"]["1"]["pilot_covered"]


def test_a_dropped_market_is_replayed_before_it_is_sold(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START - 20000, api=api, s=Settings())
    api.market["accepting_orders"] = False
    log = snapshot.run(tmp_path, now=T_START + 86400 - 20000, api=api, s=Settings())
    assert log["fills"] > 0  # the last day of trades was replayed first
    day = snapshot.utc_day(T_START + 86400 - 20000)
    rows = [json.loads(line) for line in (tmp_path / "days" / day / "closeouts.jsonl").read_text().splitlines()]
    assert {r["level"] for r in rows} == {0, 1, 2}
    assert CID not in json.loads((tmp_path / "state.json").read_text())["markets"]


def test_leaving_the_pilot_closes_the_position_as_pilot_and_restarts_it(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings(pilot_markets=1))
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["info"]["pilot"]
    state["markets"][CID]["positions"]["1"].update({"yes": 20, "yes_cost": 11.6, "cash": -11.6})
    state["markets"][CID]["trades_until"] = T_START + 86400 - snapshot.TRADE_SETTLE_S
    (tmp_path / "state.json").write_text(json.dumps(state))
    snapshot.run(tmp_path, now=T_START + 86400, api=api, s=Settings(pilot_markets=0))
    day = snapshot.utc_day(T_START + 86400)
    rows = [json.loads(line) for line in (tmp_path / "days" / day / "closeouts.jsonl").read_text().splitlines()]
    assert all(r["pilot"] for r in rows) and len(rows) == 3
    m = json.loads((tmp_path / "state.json").read_text())["markets"][CID]
    assert not m["info"]["pilot"] and m["positions"]["1"]["yes"] == 0 and m["positions"]["1"]["cash"] == 0


def test_trades_without_a_recent_midpoint_mark_a_gap(tmp_path, fx):
    class NoHistoryApi(FakeApi):
        def price_history(self, token, start, end):
            return []
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=NoHistoryApi(fx), s=Settings())
    assert any("no recent midpoint" in e for e in log["errors"])
    assert (tmp_path / "days" / snapshot.utc_day(T_START) / "gaps.jsonl").exists()


def test_an_unreadable_record_is_skipped_and_marks_a_gap(tmp_path, fx):
    class BadTradeApi(FakeApi):
        def trades_since(self, cid, since):
            trades, ok = super().trades_since(cid, since)
            return trades + [dict(trades[0], price=None, transaction_hash="0xbad"),
                             dict(trades[0], timestamp="soon", transaction_hash="0xbad2")], ok
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=BadTradeApi(fx), s=Settings())
    assert any("2 unreadable trade record(s)" in e for e in log["errors"]) and log["samples"] == 1
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["trades_until"] == T_START + 2400 - snapshot.TRADE_SETTLE_S  # not stuck
    assert (tmp_path / "days" / snapshot.utc_day(T_START) / "gaps.jsonl").exists()


def _rows(tmp_path, day, name):
    path = tmp_path / "days" / day / f"{name}.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def test_a_resolved_market_is_settled_at_one_dollar_or_nothing(tmp_path, fx):
    class ResolvedApi(FakeApi):
        def gamma_markets(self, cids):
            g = dict(self.fx("gamma_market"), closed=True, outcomePrices='["0", "1"]')  # NO won
            return {CID: g}
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings(pilot_markets=1))
    state = json.loads((tmp_path / "state.json").read_text())
    state["markets"][CID]["positions"]["1"].update({"yes": 20, "yes_cost": 11.6, "no": 5, "no_cost": 2.0,
                                                    "cash": -13.6})
    state["markets"][CID]["trades_until"] = T_START + 2400 - snapshot.TRADE_SETTLE_S
    (tmp_path / "state.json").write_text(json.dumps(state))
    snapshot.run(tmp_path, now=T_START + 2400, api=ResolvedApi(fx), s=Settings(pilot_markets=1))
    rows = _rows(tmp_path, snapshot.utc_day(T_START), "closeouts")
    row1 = next(r for r in rows if r["level"] == 1)
    assert row1["pilot"] and row1["received"] == 5 and row1["value_after"] == round(-13.6 + 5, 6)
    assert CID not in json.loads((tmp_path / "state.json").read_text())["markets"]


def test_resolution_needs_a_settled_price():
    g = {"closed": True, "outcomePrices": '["0.6", "0.4"]', "clobTokenIds": '["y", "n"]'}
    assert snapshot.resolved_yes_value(g, "y") is None
    assert snapshot.resolved_yes_value(dict(g, outcomePrices='["1", "0"]'), "y") == 1.0
    assert snapshot.resolved_yes_value(dict(g, outcomePrices='["1", "0"]'), "n") == 0.0
    assert snapshot.resolved_yes_value(dict(g, closed=False, outcomePrices='["1", "0"]'), "y") is None


def test_a_leaving_market_without_a_book_is_closed_out_after_a_few_tries(tmp_path, fx):
    class NoBookApi(FakeApi):
        def books(self, tokens):
            return {}
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings())
    nobook = NoBookApi(fx)
    nobook.market["accepting_orders"] = False
    day2 = T_START + 86400
    for i in range(snapshot.CLOSEOUT_TRIES):
        snapshot.run(tmp_path, now=day2 + i * 2400, api=nobook, s=Settings())
        still = CID in json.loads((tmp_path / "state.json").read_text())["markets"]
        assert still == (i < snapshot.CLOSEOUT_TRIES - 1)
    assert {r["level"] for r in _rows(tmp_path, snapshot.utc_day(day2), "closeouts")} == {0, 1, 2}


def test_time_without_a_book_is_sampled_as_no_reward(tmp_path, fx):
    class NoBookApi(FakeApi):
        def books(self, tokens):
            return {}
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings(pilot_markets=1))
    log = snapshot.run(tmp_path, now=T_START + 2400, api=NoBookApi(fx), s=Settings(pilot_markets=1))
    assert log["samples"] == 1
    sample = _rows(tmp_path, snapshot.utc_day(T_START), "samples")[0]
    assert sample["no_book"] and sample["dt"] == 2400
    assert all(lv["est_low"] == 0 and lv["value"] is None for lv in sample["levels"].values())


def test_a_hole_in_the_price_history_marks_a_gap(tmp_path, fx):
    class HoleApi(FakeApi):
        def price_history(self, token, start, end):
            return [(t, p) for t, p in super().price_history(token, start, end)
                    if not T_START + 600 < t < T_START + 1500]
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=HoleApi(fx), s=Settings())
    assert any("hole in the price history" in e for e in log["errors"])


def test_a_lagging_price_history_holds_the_window_back(tmp_path, fx):
    class LagApi(FakeApi):
        def price_history(self, token, start, end):
            return [(t, p) for t, p in super().price_history(token, start, end) if t <= end - 400]
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=LagApi(fx), s=Settings())
    assert log["errors"] == []
    m = json.loads((tmp_path / "state.json").read_text())["markets"][CID]
    history_end = max(t for t, _ in FakeApi(fx).price_history("", 0, T_START + 2400 - 400))
    assert m["trades_until"] == history_end < T_START + 2400 - snapshot.TRADE_SETTLE_S


def test_a_gap_is_filed_under_every_day_its_window_touches(tmp_path, fx):
    midnight = 1792195200  # 2026-10-17 00:00 UTC, inside the fixture data
    snapshot.run(tmp_path, now=midnight - 1800, api=FakeApi(fx), s=Settings())
    state = json.loads((tmp_path / "state.json").read_text())
    state["watchlist_day"] = snapshot.utc_day(midnight + 1200)  # no refresh: keep the same market
    (tmp_path / "state.json").write_text(json.dumps(state))
    snapshot.run(tmp_path, now=midnight + 1200, api=FakeApi(fx, cut_short=True), s=Settings())
    assert _rows(tmp_path, snapshot.utc_day(midnight - 1), "gaps") and _rows(tmp_path, snapshot.utc_day(midnight), "gaps")


def test_a_trades_only_replay_is_kept_alongside(tmp_path, fx):
    api = FakeApi(fx)
    snapshot.run(tmp_path, now=T_START, api=api, s=Settings(pilot_markets=1))
    state = json.loads((tmp_path / "state.json").read_text())
    del state["markets"][CID]["positions_trades_only"]  # state written before the comparison existed
    (tmp_path / "state.json").write_text(json.dumps(state))
    log = snapshot.run(tmp_path, now=T_START + 2400, api=api, s=Settings(pilot_markets=1))
    assert log["errors"] == []
    m = json.loads((tmp_path / "state.json").read_text())["markets"][CID]
    assert set(m["positions_trades_only"]) == {"0", "1", "2"}
    sample = _rows(tmp_path, snapshot.utc_day(T_START), "samples")[-1]
    assert all(lv["value_trades_only"] is not None for lv in sample["levels"].values())
    api.market["accepting_orders"] = False
    snapshot.run(tmp_path, now=T_START + 86400, api=api, s=Settings(pilot_markets=1))
    rows = _rows(tmp_path, snapshot.utc_day(T_START + 86400), "closeouts")
    assert len(rows) == 3 and all("value_after_trades_only" in r for r in rows)


def test_a_report_error_is_saved_with_the_run(tmp_path, fx, monkeypatch):
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    def broken(*args, **kwargs):
        raise KeyError("pilot_income")
    monkeypatch.setattr(snapshot.report, "build", broken)
    snapshot.run(tmp_path, now=T_START + 2400, api=FakeApi(fx), s=Settings())
    runs = _rows(tmp_path, snapshot.utc_day(T_START), "runs")
    assert any("report: KeyError" in e for e in runs[-1]["errors"])


def test_settings_accept_a_count_written_with_a_decimal_point():
    assert snapshot.settings_from_env({"PM_WATCH_MARKETS": "25.0"}).watch_markets == 25


def test_a_market_that_fails_every_run_skips_its_window_with_a_gap(tmp_path, fx):
    class BadHistoryApi(FakeApi):
        def price_history(self, token, start, end):
            raise pmapi.ApiError("bad history")
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    for i in range(1, snapshot.MAX_FAILED_RUNS + 1):
        snapshot.run(tmp_path, now=T_START + i * 600, api=BadHistoryApi(fx), s=Settings())
        m = json.loads((tmp_path / "state.json").read_text())["markets"][CID]
        stuck = m["trades_until"] == T_START - snapshot.TRADE_SETTLE_S
        assert stuck == (i < snapshot.MAX_FAILED_RUNS)
    gaps = _rows(tmp_path, snapshot.utc_day(T_START), "gaps")
    assert any("failed runs" in g["reason"] for g in gaps)


def test_rewards_earned_today_wait_for_tomorrow_to_count_in_the_budget(tmp_path, fx):
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings(pilot_markets=1))
    snapshot.run(tmp_path, now=T_START + 2400, api=FakeApi(fx), s=Settings(pilot_markets=1))
    pos = json.loads((tmp_path / "state.json").read_text())["markets"][CID]["positions"]["1"]
    assert pos["pending_rewards"] > 0 and pos["reward_credit"] == 0
    assert pos["credit_day"] == snapshot.utc_day(T_START + 2400)
    runs = _rows(tmp_path, snapshot.utc_day(T_START), "runs")
    assert runs[-1]["plan"] == {"pilot_markets": 1, "budget_per_market_usd": 20.0, "pilot_level": 1}
