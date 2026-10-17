import json

import pmapi
import snapshot
from selection import Settings

CID = "0xb0ea6c2f159bac649d481edc3d471fd8b9a912793ce16585e2a2333ad98821c3"
T_START = 1792190000  # inside the fixture's price history and trades
T_END = 1792209018    # when the fixture book was taken


class FakeApi:
    """Serves the recorded live responses in tests/fixtures."""

    def __init__(self, fx, fail_trades=False):
        self.fx = fx
        self.fail_trades = fail_trades
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

    def taker_trades_since(self, cid, since):
        if self.fail_trades:
            raise pmapi.ApiError("boom")
        trades = [t for t in self.fx("trades_taker") if t["timestamp"] > since]
        return sorted(trades, key=lambda t: t["timestamp"]), True


def test_two_runs_record_samples_fills_and_a_report(tmp_path, fx):
    api = FakeApi(fx)
    s = Settings(pilot_markets=1)
    log1 = snapshot.run(tmp_path, now=T_START, api=api, s=s)
    assert log1["errors"] == [] and log1["markets"] == 1 and log1["samples"] == 1
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["watchlist_day"] == snapshot.utc_day(T_START)
    assert state["markets"][CID]["info"]["fee_rate"] == 0.04

    log2 = snapshot.run(tmp_path, now=T_END, api=api, s=s)
    assert log2["errors"] == []
    samples = [json.loads(line) for d in sorted((tmp_path / "days").iterdir())
               for line in (d / "samples.jsonl").read_text().splitlines()]
    assert len(samples) == 2 and samples[1]["dt"] == snapshot.MAX_SAMPLE_DT_S
    for lv in samples[1]["levels"].values():
        assert 0 <= lv["share_low"] <= lv["share_high"] <= 1
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["markets"][CID]["trades_until"] == T_END - snapshot.TRADE_SETTLE_S
    replayed = [t for t in fx("trades_taker") if T_START - 120 < t["timestamp"] <= T_END - 120]
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
    (tmp_path / "state.json").write_text(json.dumps(state))
    api.market["accepting_orders"] = False  # gone from tomorrow's list
    snapshot.run(tmp_path, now=T_START + 86400, api=api, s=Settings())
    day = snapshot.utc_day(T_START + 86400)
    rows = [json.loads(line) for line in (tmp_path / "days" / day / "closeouts.jsonl").read_text().splitlines()]
    row0 = next(r for r in rows if r["level"] == 0)
    assert row0["received"] == 20 * 0.58  # best bid in the fixture book
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
