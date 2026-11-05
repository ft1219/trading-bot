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


def test_range_prob_sums_to_one_and_centres():
    members = [10.0, 11.0, 12.0]
    ranges = [(-math.inf, 9.5), (9.5, 10.5), (10.5, 11.5), (11.5, 12.5), (12.5, math.inf)]
    probs = [W.range_prob(members, lo, hi, 1.0) for lo, hi in ranges]
    assert sum(probs) == pytest.approx(1.0)
    assert probs[2] == max(probs)


def test_ensemble_parsing():
    body = {"daily": {"time": ["2026-11-06"], "temperature_2m_max_ecmwf_ifs025_ensemble": [11.0],
                      "temperature_2m_max_member01_ecmwf_ifs025_ensemble": [12.0],
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


def _temp_event():
    mk = []
    for i, label in enumerate(["13°C or below", "14°C", "15°C", "16°C or higher"]):
        m = {"conditionId": f"c{i}", "groupItemTitle": label, "question": f"Will it be {label}?",
             "active": True, "closed": False, "acceptingOrders": True, "enableOrderBook": True,
             "endDate": "2026-11-06T12:00:00Z", "clobTokenIds": f'["t{i}y", "t{i}n"]', "outcomes": '["Yes", "No"]',
             "bestBid": 0.20, "bestAsk": 0.22, "feesEnabled": False,
             "description": "recorded at Test Airport (ZZZZ) on 6 Nov '26."}
        mk.append(m)
    return {"id": "E9", "title": "Highest temperature in Testville on November 6?", "endDate": "2026-11-06T12:00:00Z", "markets": mk}


def test_forecast_picks_buys_where_forecast_disagrees():
    ev = _temp_event()
    # every member says 18°C, so "16°C or higher" is near-certain; the market prices each range at 22c
    now = lab.parse_ts("2026-11-05T00:00:00Z")

    def fetch(url, body):
        if "stationinfo" in url:
            return [{"icaoId": "ZZZZ", "lat": 1.0, "lon": 2.0}]
        if "ensemble" in url:
            return {"utc_offset_seconds": 3600, "daily": {"time": ["2026-11-05", "2026-11-06"], "temperature_2m_max_x": [1.0, 18.0],
                              **{f"temperature_2m_max_member{i:02d}_x": [1.0, 18.0] for i in range(1, 30)}}}
        raise AssertionError(url)

    views = {m["conditionId"]: lab.market_view(m, now) for m in W.as_markets([ev])}
    state = {}
    picks, notes = W.forecast_picks([ev], views, state, now, fetch)
    assert len(picks) == 1
    v, idx, cap, prob = picks[0]
    assert v["groupItemTitle"] == "16°C or higher" and idx == 0 and prob > 0.9 and cap <= W.MAX_PRICE
    assert state["stations"]["ZZZZ"] == [1.0, 2.0]
    assert notes[0]["edge"] > 0.5
    # once the local day has begun the market may already know the answer: no trade
    late = lab.parse_ts("2026-11-05T23:30:00Z")  # 00:30 local on the 6th
    assert W.forecast_picks([ev], views, {}, late, fetch) == ([], [])
