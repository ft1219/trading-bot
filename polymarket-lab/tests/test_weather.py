import math

import pytest

import lab
import weather as W

NOW = 1_793_000_000.0


def test_parse_range():
    assert W.parse_range("16°C") == (15.5, 16.5, "C")
    assert W.parse_range("13°C or below") == (-math.inf, 13.5, "C")
    assert W.parse_range("23°C or higher") == (22.5, math.inf, "C")
    assert W.parse_range("94-95°F") == (93.5, 95.5, "F")
    assert W.parse_range("Yes") is None


def test_parse_event():
    ev = {"title": "Highest temperature in Paris on November 6?", "endDate": "2026-11-06T12:00:00Z",
          "markets": [{"description": "... at Paris-Le Bourget Airport (LFPB) on 6 Nov '26."}]}
    assert W.parse_event(ev) == ("max", "2026-11-06", "LFPB")
    assert W.parse_event({"title": "Who wins?", "endDate": "2026-11-06T12:00:00Z", "markets": []}) is None
    assert W.is_temperature_event("Lowest temperature in Tokyo on November 7?")
    assert not W.is_temperature_event("Bitcoin Up or Down - November 6, 2AM ET")


def test_range_prob_sums_to_one_and_centres():
    members = [10.0, 11.0, 12.0]
    ranges = [(-math.inf, 9.5), (9.5, 10.5), (10.5, 11.5), (11.5, 12.5), (12.5, math.inf)]
    probs = [W.range_prob(members, lo, hi, 1.0) for lo, hi in ranges]
    assert sum(probs) == pytest.approx(1.0)
    assert probs[2] == max(probs)


def test_ensemble_parsing():
    body = {"daily": {"time": ["2026-11-06"], "temperature_2m_max_ecmwf_ifs025_ensemble": [11.0],
                      "temperature_2m_max_member01_ecmwf_ifs025_ensemble": [12.04],
                      "temperature_2m_min_ncep_gefs_seamless": [3.0], "other": [1]}}
    fc = W.ensemble(1.0, 2.0, fetch=lambda u, b: body)
    assert fc == {"offset": 0, "days": {"2026-11-06": {"max": [11.0, 12.0], "min": [3.0]}}}


def test_day_started_uses_local_time():
    nov6_utc = lab.parse_ts("2026-11-06T00:00:00Z")
    assert not W.day_started("2026-11-06", 0, nov6_utc - 1)
    assert W.day_started("2026-11-06", 0, nov6_utc)
    # Tokyo (UTC+9) starts 6 November at 15:00 UTC on the 5th
    assert W.day_started("2026-11-06", 9 * 3600, nov6_utc - 9 * 3600)
    assert not W.day_started("2026-11-06", 9 * 3600, nov6_utc - 9 * 3600 - 60)


def _temp_event(prices=None):
    mk = []
    labels = ["13°C or below", "14°C", "15°C", "16°C or higher"]
    for i, label in enumerate(labels):
        bid, ask = (prices or {}).get(label, (0.20, 0.22))
        m = {"conditionId": f"c{i}", "groupItemTitle": label, "question": f"Will it be {label}?",
             "active": True, "closed": False, "acceptingOrders": True, "enableOrderBook": True,
             "endDate": "2026-11-06T12:00:00Z", "clobTokenIds": f'["t{i}y", "t{i}n"]', "outcomes": '["Yes", "No"]',
             "bestBid": bid, "bestAsk": ask, "feesEnabled": False, "orderMinSize": 5,
             "description": "recorded at Test Airport (ZZZZ) on 6 Nov '26."}
        if bid is None:
            del m["bestBid"]
        mk.append(m)
    return {"id": "E9", "title": "Highest temperature in Testville on November 6?", "endDate": "2026-11-06T12:00:00Z", "markets": mk}


def _fetch_with(members):
    def fetch(url, body):
        if "stationinfo" in url:
            return [{"icaoId": "ZZZZ", "lat": 1.0, "lon": 2.0}]
        if "ensemble" in url:
            return {"utc_offset_seconds": 3600, "daily": {"time": ["2026-11-05", "2026-11-06"],
                    **{f"temperature_2m_max_member{i:02d}_x": [1.0, v] for i, v in enumerate(members)}}}
        raise AssertionError(url)
    return fetch


def test_forecast_picks_buys_where_forecast_disagrees():
    ev = _temp_event()
    # every member says 18°C, so "16°C or higher" is near-certain; the market prices each range at 22c
    now = lab.parse_ts("2026-11-05T00:00:00Z")
    fetch = _fetch_with([18.0] * 30)
    views = {m["conditionId"]: lab.market_view(m, now) for m in W.as_markets([ev])}
    state = {}
    res = W.forecast_picks([ev], views, state, now, fetch)
    assert len(res["picks"]) == 1 and not res["problems"]
    v, idx, cap, note = res["picks"][0]
    assert v["groupItemTitle"] == "16°C or higher" and idx == 0 and note["forecast_chance"] > 0.9 and cap <= W.MAX_PRICE
    assert note["lead_h"] == pytest.approx(23.0) and note["station"] == "ZZZZ"
    assert state["stations"]["ZZZZ"] == [1.0, 2.0] and state["forecasts"]["ZZZZ"]["at"] == int(now)
    assert res["notes"][0]["edge"] > 0.5
    # one calibration row per event per day, with every range in it
    assert len(res["rows"]) == 1 and len(res["rows"][0]["bins"]) == 4 and res["rows"][0]["sd"] == 0
    assert W.forecast_picks([ev], views, state, now + 600, fetch)["rows"] == []
    # once the local day has begun the market may already know the answer: no trade
    late = lab.parse_ts("2026-11-05T23:30:00Z")  # 00:30 local on the 6th
    assert W.forecast_picks([ev], views, {}, late, fetch)["picks"] == []


def test_held_events_still_get_their_daily_snapshot(tmp_path, monkeypatch):
    """lab.run passes every temperature event to forecast_picks and drops held events from the picks only."""
    import json

    def run_serial(calls, workers=8):
        out = {}
        for k, fn in calls.items():
            try:
                out[k] = fn()
            except Exception as e:  # noqa: BLE001
                out[k] = e
        return out

    monkeypatch.setattr(lab.pmapi, "parallel", run_serial)
    ev = _temp_event({"16°C or higher": (0.20, 0.22)})
    members = [16.5] * 60 + [15.5] * 22  # the forecast likes "16 or higher" at 22c

    def fetch(url, body):
        if "/markets?" in url and "closed=true" in url:
            return []
        if "/events?" in url:
            return [ev] if "offset=0" in url else []
        if url.endswith("/books"):
            return [{"asset_id": b["token_id"], "asks": [{"price": "0.22", "size": "500"}]} for b in body]
        if "stationinfo" in url:
            return [{"icaoId": "ZZZZ", "lat": 1.0, "lon": 2.0}]
        if "ensemble" in url:  # a station five hours behind UTC: its 6 November starts at 05:00 UTC
            return {"utc_offset_seconds": -18000, "daily": {"time": ["2026-11-05", "2026-11-06"],
                    **{f"temperature_2m_max_member{i:02d}_x": [1.0, v] for i, v in enumerate(members)}}}
        raise AssertionError(url)

    def weather_trades():
        rows = []
        for f in sorted((tmp_path / "trades").glob("*.jsonl")):
            rows += [json.loads(line) for line in f.read_text().splitlines()]
        return [t for t in rows if t["strategy"] == "weather_forecast"]

    now = lab.parse_ts("2026-11-05T06:00:00Z")
    row = lab.run(tmp_path, now, fetch, seed=1)
    assert not row["problems"] and len(weather_trades()) == 1
    state = json.loads((tmp_path / "state.json").read_text())
    assert "E9" in state["traded_events"]["weather_forecast"]
    # the next UTC day, still before the station's local day: the event is held, so no second buy,
    # but its forecast snapshot for the new day is still written
    row2 = lab.run(tmp_path, lab.parse_ts("2026-11-06T02:00:00Z"), fetch, seed=2)
    assert not row2["problems"] and len(weather_trades()) == 1
    rows = []
    for f in sorted((tmp_path / "forecasts").glob("*.jsonl")):
        rows += [json.loads(line) for line in f.read_text().splitlines()]
    assert len([r for r in rows if r["event_id"] == "E9"]) == 2


def test_smoothing_alone_never_sells_the_favourite():
    # a tight ensemble: all 30 members say about 15°C, and the market agrees (15°C at 50-52c)
    ev = _temp_event({"15°C": (0.50, 0.52), "14°C": (0.15, 0.17), "16°C or higher": (0.15, 0.17), "13°C or below": (0.10, 0.12)})
    now = lab.parse_ts("2026-11-05T00:00:00Z")
    views = {m["conditionId"]: lab.market_view(m, now) for m in W.as_markets([ev])}
    res = W.forecast_picks([ev], views, {}, now, _fetch_with([15.0 + 0.3 * ((i % 3) - 1) for i in range(30)]))
    assert res["picks"] == []  # the old rule sold "15°C" here, claiming ~67% for No from the smoothing alone


def test_yes_side_is_judged_when_the_bid_is_missing():
    ev = _temp_event({"16°C or higher": (None, 0.22)})
    now = lab.parse_ts("2026-11-05T00:00:00Z")
    views = {m["conditionId"]: lab.market_view(m, now) for m in W.as_markets([ev])}
    res = W.forecast_picks([ev], views, {}, now, _fetch_with([18.0] * 30))
    assert len(res["picks"]) == 1 and res["picks"][0][0]["groupItemTitle"] == "16°C or higher" and res["picks"][0][1] == 0


def test_forecast_cache_and_fetch_budget(monkeypatch):
    calls = []

    def fetch(url, body):
        calls.append(url)
        if "stationinfo" in url:
            return [{"icaoId": i, "lat": 1.0, "lon": 2.0} for i in ("AAAA", "BBBB", "CCCC")]
        if "ensemble" in url and len([c for c in calls if "ensemble" in c]) > 2:
            raise lab.pmapi.ApiError("429")
        return {"utc_offset_seconds": 0, "daily": {"time": ["2026-11-06"], "temperature_2m_max_x": [10.0]}}

    monkeypatch.setattr(W, "MAX_FETCH_PER_RUN", 5)
    coords = W.station_coords(["AAAA", "BBBB", "CCCC"], {}, fetch)
    cache, problems = {}, []
    now = lab.parse_ts("2026-11-05T00:00:00Z")
    fcs = W.forecasts_for(["AAAA", "BBBB", "CCCC"], coords, cache, now, fetch, problems)
    assert fcs["AAAA"] and fcs["BBBB"] and fcs["CCCC"] is None  # third call failed: no more fetching this run
    assert len(problems) == 1 and "CCCC" in problems[0]
    n = len(calls)
    # within the TTL nothing is fetched again; after it, a fresh fetch (which fails here) falls back to the stale copy
    assert W.forecasts_for(["AAAA"], coords, cache, now + 3600, fetch, [])["AAAA"] and len(calls) == n
    assert W.forecasts_for(["AAAA"], coords, cache, now + 4 * 3600, fetch, [])["AAAA"] and len(calls) == n + 1
    assert W.forecasts_for(["AAAA"], coords, cache, now + 7 * 3600, fetch, [])["AAAA"] is None
