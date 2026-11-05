"""
Daily temperature markets ("Highest temperature in Paris on November 6?").

Each event has about 11 ranges ("13°C or below", "14°C", ..., "23°C or
higher"); exactly one wins. It resolves on the highest (or lowest) hourly
METAR reading at one named airport, rounded to a whole degree (half up), on
that airport's local date.

The history check (Aug-Nov 2026) found these markets less well priced than
sports: buying the 80-95 cent side two days out earned +3% to +5% a trade,
both in the months used to look and in the month held back. This module adds
an informed version: compare each range's price with the chance a weather
forecast gives it, and buy where the forecast disagrees by a lot.

Forecast: Open-Meteo's free ensemble API (ECMWF 51 members + GFS 31 members),
no key needed. Each member's daily max/min, plus a spread of SIGMA_C for the
gap between a model grid box and one airport thermometer, gives a chance for
each range.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import urllib.parse

import pmapi

ENSEMBLE = "https://ensemble-api.open-meteo.com/v1/ensemble"
STATIONS = "https://aviationweather.gov/api/data/stationinfo"
MODELS = "ecmwf_ifs025,gfs_seamless"
SIGMA_C = 1.2  # grid box vs one airport, and hourly readings vs the true peak
MIN_EDGE = 0.10  # forecast chance minus asking price
MIN_PROB = 0.20  # never buy a side the forecast gives less than this
MAX_PRICE = 0.95
# Trade only while the station's local observation day has not started: once
# it has, the market can see the real readings and the forecast is stale. The
# first live run bought against markets that already knew the day's result.
LEAD_HOURS = 0.0

_RANGE = re.compile(r"^\s*(-?\d+)(?:\s*-\s*(-?\d+))?\s*°\s*([CF])(?:\s+or\s+(below|lower|higher|above))?\s*$", re.I)
_TITLE = re.compile(r"^(Highest|Lowest) temperature in (.+?) on ([A-Za-z]+ \d{1,2})\??$")
_ICAO = re.compile(r"\(([A-Z]{4})\)")


def parse_range(label: str):
    """'16°C' -> (15.5, 16.5, 'C'); '13°C or below' -> (-inf, 13.5, 'C'); '94-95°F' -> (93.5, 95.5, 'F')."""
    m = _RANGE.match(label or "")
    if not m:
        return None
    a, b, unit, tail = int(m.group(1)), m.group(2), m.group(3).upper(), (m.group(4) or "").lower()
    if tail in ("below", "lower"):
        return (-math.inf, a + 0.5, unit)
    if tail in ("higher", "above"):
        return (a - 0.5, math.inf, unit)
    hi = int(b) if b is not None else a
    return (a - 0.5, hi + 0.5, unit)


def parse_event(ev: dict):
    """(kind 'max'|'min', local date 'YYYY-MM-DD', ICAO) or None."""
    m = _TITLE.match((ev.get("title") or "").strip())
    if not m:
        return None
    kind = "max" if m.group(1) == "Highest" else "min"
    end = (ev.get("endDate") or "")[:10]
    try:
        year = int(end[:4])
        day = dt.datetime.strptime(f"{m.group(3)} {year}", "%B %d %Y").date()
    except ValueError:
        return None
    desc = " ".join((mk.get("description") or "") for mk in (ev.get("markets") or [])[:1])
    icao = _ICAO.search(desc)
    if not icao:
        return None
    return kind, day.isoformat(), icao.group(1)


def _phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def range_prob(members: list[float], lo: float, hi: float, sigma: float) -> float:
    if not members:
        return 0.0
    tot = 0.0
    for v in members:
        p_hi = 1.0 if hi == math.inf else _phi((hi - v) / sigma)
        p_lo = 0.0 if lo == -math.inf else _phi((lo - v) / sigma)
        tot += p_hi - p_lo
    return tot / len(members)


def station_coords(icaos, cache: dict, fetch=pmapi.http_json) -> dict:
    need = sorted({i for i in icaos if i not in cache})
    for k in range(0, len(need), 20):
        rows = fetch(f"{STATIONS}?ids={','.join(need[k:k + 20])}&format=json", None)
        for r in rows if isinstance(rows, list) else []:
            try:
                cache[r["icaoId"]] = [float(r["lat"]), float(r["lon"])]
            except (KeyError, TypeError, ValueError):
                continue
    return cache


def ensemble(lat: float, lon: float, fetch=pmapi.http_json) -> dict:
    """
    {'offset': local UTC offset in seconds, 'days': {'YYYY-MM-DD': {'max': [members], 'min': [members]}}},
    local dates, °C.
    """
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "models": MODELS, "timezone": "auto",
                                "daily": "temperature_2m_max,temperature_2m_min", "forecast_days": 5})
    body = fetch(f"{ENSEMBLE}?{q}", None)
    daily = (body or {}).get("daily") if isinstance(body, dict) else None
    if not isinstance(daily, dict) or not isinstance(daily.get("time"), list):
        raise pmapi.ApiError("ensemble: unexpected shape")
    out = {d: {"max": [], "min": []} for d in daily["time"]}
    try:
        offset = int(body.get("utc_offset_seconds") or 0)
    except (TypeError, ValueError):
        offset = 0
    for key, vals in daily.items():
        if key == "time":
            continue
        # the control run is named after the model; perturbed runs carry "memberNN"
        kind = "max" if key.startswith("temperature_2m_max") else "min" if key.startswith("temperature_2m_min") else None
        if not kind or not isinstance(vals, list):
            continue
        for d, v in zip(daily["time"], vals):
            if isinstance(v, (int, float)):
                out[d][kind].append(float(v))
    return {"offset": offset, "days": out}


def day_started(day: str, offset: int, now: float) -> bool:
    """True once the station's local date `day` has begun (minus LEAD_HOURS)."""
    start = dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc).timestamp() - offset
    return now >= start - LEAD_HOURS * 3600


def to_unit(members: list[float], unit: str) -> list[float]:
    return [v * 9 / 5 + 32 for v in members] if unit == "F" else members


def list_events(now: float, fetch=pmapi.http_json) -> list[dict]:
    lo = dt.datetime.fromtimestamp(now, dt.timezone.utc)
    hi = lo + dt.timedelta(days=4)
    out = []
    for off in range(0, 1000, 100):
        q = urllib.parse.urlencode({"tag_slug": "daily-temperature", "active": "true", "closed": "false",
                                    "limit": 100, "offset": off,
                                    "end_date_min": lo.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                    "end_date_max": hi.strftime("%Y-%m-%dT%H:%M:%SZ")})
        page = fetch(f"{pmapi.GAMMA}/events?{q}", None)
        if not isinstance(page, list):
            raise pmapi.ApiError("/events: unexpected shape")
        out.extend(page)
        if len(page) < 100:
            break
    return out


def as_markets(events: list[dict]) -> list[dict]:
    """The events' markets, with the event attached the way /markets returns it."""
    out = []
    for ev in events:
        for m in ev.get("markets") or []:
            m = dict(m)
            m.setdefault("events", [{"id": ev.get("id"), "title": ev.get("title")}])
            out.append(m)
    return out


def forecast_picks(events: list[dict], views_by_cid: dict, state: dict, now: float, fetch=pmapi.http_json) -> tuple[list, list]:
    """
    For each event, the one range and side where the forecast's chance beats
    the asking price by the most (at least MIN_EDGE). Returns
    (picks [(view, outcome_index, price_cap, prob)], notes).
    """
    cache = state.setdefault("stations", {})
    parsed = {}
    for ev in events:
        info = parse_event(ev)
        if info:
            parsed[str(ev.get("id"))] = (ev, info)
    station_coords({info[2] for _, info in parsed.values()}, cache, fetch)
    fc_cache: dict = {}
    picks, notes = [], []
    for eid, (ev, (kind, day, icao)) in parsed.items():
        if icao not in cache:
            continue
        if icao not in fc_cache:
            try:
                fc_cache[icao] = ensemble(*cache[icao], fetch=fetch)
            except pmapi.ApiError:
                fc_cache[icao] = None
        fc = fc_cache[icao]
        if not fc or day not in fc["days"] or len(fc["days"][day][kind]) < 20:
            continue
        if day_started(day, fc["offset"], now):
            continue
        members = fc["days"][day][kind]
        best = None
        for m in ev.get("markets") or []:
            v = views_by_cid.get(m.get("conditionId"))
            rng = parse_range(m.get("groupItemTitle") or "")
            if not v or not rng:
                continue
            lo, hi, unit = rng
            sigma = SIGMA_C * (1.8 if unit == "F" else 1.0)
            p = range_prob(to_unit(members, unit), lo, hi, sigma)
            try:
                bid, ask = float(v["bestBid"]), float(v["bestAsk"])
            except (KeyError, TypeError, ValueError):
                continue
            for idx, prob, price in ((0, p, ask), (1, 1 - p, 1 - bid)):
                edge = prob - price
                if prob >= MIN_PROB and 0 < price <= MAX_PRICE and edge >= MIN_EDGE and (best is None or edge > best[3]):
                    best = (v, idx, round(min(MAX_PRICE, prob - MIN_EDGE / 2), 3), edge, prob)
        if best:
            v, idx, cap, edge, prob = best
            picks.append((v, idx, cap, prob))
            notes.append({"event": ev.get("title"), "range": v.get("groupItemTitle"), "side": "Yes" if idx == 0 else "No",
                          "forecast_chance": round(prob, 3), "edge": round(edge, 3)})
    return picks, notes
