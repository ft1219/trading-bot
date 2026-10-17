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


def test_one_bad_record_does_not_stop_the_other_markets(tmp_path, fx):
    class BadTradeApi(FakeApi):
        def trades_since(self, cid, since):
            trades, ok = super().trades_since(cid, since)
            return trades + [dict(trades[0], price=None, transaction_hash="0xbad")], ok
    snapshot.run(tmp_path, now=T_START, api=FakeApi(fx), s=Settings())
    log = snapshot.run(tmp_path, now=T_START + 2400, api=BadTradeApi(fx), s=Settings())
    assert any("0xb0ea6c2f" in e for e in log["errors"])
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["trades_until"] == T_START - snapshot.TRADE_SETTLE_S  # retried next run
