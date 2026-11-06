"""
Daily temperature markets ("Highest temperature in Paris on November 6?").

Each event has about 11 ranges ("13°C or below", "14°C", ..., "23°C or
higher"); exactly one wins. It resolves on the highest (or lowest) hourly
METAR reading at one named airport, rounded to a whole degree (half up), on
that airport's local date.

This is the one strategy with an information source of its own: compare
each range's price with the chance a weather forecast gives it, and buy
where the forecast disagrees by a lot. (The history replay that first
pointed at these markets turned out to be an artifact of near-empty books,
see README; the live record is the only evidence for or against this idea.)

Forecast: Open-Meteo's free ensemble API (ECMWF 51 members + GFS 31 members),
no key needed, non-commercial terms. A range's chance is computed twice:
from the members as they are ("raw"), and with a spread of SIGMA_C added to
each member for the gap between a model grid box and one airport
thermometer ("smoothed"). A side is bought only when BOTH versions give it
at least MIN_EDGE more than the price. The smoothing alone can never make a
case for a trade: it caps any single degree's chance at about a third, so
on its own it would "disagree" with every market favourite priced above
about 40 cents, which is not a forecast, it is a constant. The same cap
means the smoothed test rarely lets a Yes buy through on a single-degree
range (that needs an ask of about 22 cents or less), so in practice the
rule almost always buys No against an overpriced range, usually the market
favourite, and buys Yes only on open-ended or wide ranges. Unlike the rules
in strategies.py it applies no bid-ask gap test: the forecast, not the
quote, is its signal, and it pays the real asking price of the side it buys
(for No, that is one minus the Yes bid).
"""
from __future__ import annotations

import datetime as dt
import math
import re
import statistics
import urllib.parse

import pmapi

ENSEMBLE = "https://ensemble-api.open-meteo.com/v1/ensemble"
STATIONS = "https://aviationweather.gov/api/data/stationinfo"
MODELS = "ecmwf_ifs025,gfs_seamless"
SIGMA_C = 1.2  # grid box vs one airport, and hourly readings vs the true peak
SIGMA_RAW_C = 0.1  # "raw": the members as they are (a hair of width so a member on a boundary splits)
MIN_EDGE = 0.10  # forecast chance minus asking price, raw and smoothed
MIN_PROB = 0.20  # never buy a side the forecast gives less than this
MAX_PRICE = 0.95
# Trade only while the station's local observation day has not started: once
# it has, the market can see the real readings and the forecast is stale. The
# first live run bought against markets that already knew the day's result.
LEAD_HOURS = 0.0
# Open-Meteo's free tier allows 600 weighted calls a minute and 10,000 a day.
# One ensemble call for two models weighs about 16 (read from the API's
# X-RateLimit-Cost header; the published rules give no member formula). So
# each station's forecast is kept for FORECAST_TTL seconds and at most
# MAX_FETCH_PER_RUN are refreshed in a run: for 48 stations about 380 fresh
# calls a day, roughly 6,000-6,500 weighted of the 10,000 allowed, and a
# run's burst of 20 is about 330 weighted of the 600 a minute.
FORECAST_TTL = 3 * 3600
EVENT_DAYS = 3  # temperature events ending within this many days are looked at
FORECAST_DAYS = 4  # today and the next three local days, enough for EVENT_DAYS
FORECAST_STALE = 6 * 3600  # older than this: do not trade on it
MAX_FETCH_PER_RUN = 20

_RANGE = re.compile(r"^\s*(-?\d+)(?:\s*-\s*(-?\d+))?\s*°\s*([CF])(?:\s+or\s+(below|lower|higher|above))?\s*$", re.I)
_TITLE = re.compile(r"^(Highest|Lowest) temperature in (.+?) on ([A-Za-z]+ \d{1,2})\??$")
_ICAO = re.compile(r"\(([A-Z]{4})\)")


def is_temperature_event(title: str | None) -> bool:
    return bool(_TITLE.match((title or "").strip()))


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
    local dates, °C (rounded to 0.1, which is all the resolution rule needs).
    """
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "models": MODELS, "timezone": "auto",
                                "daily": "temperature_2m_max,temperature_2m_min", "forecast_days": FORECAST_DAYS})
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
                out[d][kind].append(round(float(v), 1))
    return {"offset": offset, "days": out}


def day_start(day: str, offset: int) -> float:
    """Unix time at which the station's local date `day` begins."""
    return dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc).timestamp() - offset


def day_started(day: str, offset: int, now: float) -> bool:
    """True once the station's local date `day` has begun (minus LEAD_HOURS)."""
    return now >= day_start(day, offset) - LEAD_HOURS * 3600


def to_unit(members: list[float], unit: str) -> list[float]:
    return [v * 9 / 5 + 32 for v in members] if unit == "F" else members


def as_markets(events: list[dict]) -> list[dict]:
    """The events' markets, with the event attached the way /markets returns it."""
    out = []
    for ev in events:
        for m in ev.get("markets") or []:
            m = dict(m)
            m.setdefault("events", [{"id": ev.get("id"), "title": ev.get("title")}])
            out.append(m)
    return out


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def forecasts_for(icaos: list[str], coords: dict, cache: dict, now: float, fetch, problems: list[str]) -> dict:
    """
    icao -> forecast (or None), from `cache` ({icao: {"at": ts, "fc": ...}}),
    refreshing stale entries within this run's call budget. Stops asking
    Open-Meteo after its first failure so a bad hour cannot eat the run.
    """
    out: dict = {}
    fetched = 0
    stopped = False
    for icao in icaos:
        if icao not in coords:
            continue
        entry = cache.get(icao) or {}
        age = now - float(entry.get("at") or 0)
        fc = entry.get("fc") if isinstance(entry.get("fc"), dict) else None
        if fc is None or age > FORECAST_TTL:
            if not stopped and fetched < MAX_FETCH_PER_RUN:
                fetched += 1
                try:
                    fc = ensemble(*coords[icao], fetch=fetch)
                    cache[icao] = {"at": int(now), "fc": fc}
                    age = 0.0
                except pmapi.ApiError as e:
                    stopped = True
                    problems.append(f"weather: Open-Meteo failed for {icao}, no more forecasts fetched this run: {e}"[:300])
        if fc is None or age > FORECAST_STALE:
            out[icao] = None
        else:
            out[icao] = fc
    for icao in list(cache):
        if icao not in icaos and now - float((cache.get(icao) or {}).get("at") or 0) > FORECAST_STALE:
            del cache[icao]
    return out


def forecast_picks(events: list[dict], views_by_cid: dict, state: dict, now: float, fetch=pmapi.http_json) -> dict:
    """
    For each event, the one range and side where the forecast's chance beats
    the asking price by the most, raw and smoothed (both at least MIN_EDGE).
    Returns {"picks": [(view, outcome_index, price_cap, note)], "notes": [...],
    "rows": [...], "problems": [...]}: notes are the disagreements found
    (trade or not); rows are one full forecast-versus-price snapshot per
    event per UTC day, for checking later how well calibrated the forecasts
    and the market were.
    """
    coords = state.setdefault("stations", {})
    fcache = state.setdefault("forecasts", {})
    logged = state.setdefault("forecast_logged", {})
    problems: list[str] = []
    parsed = {}
    for ev in events:
        info = parse_event(ev)
        if info:
            parsed[str(ev.get("id"))] = (ev, info)
    try:
        station_coords({info[2] for _, info in parsed.values()}, coords, fetch)
    except pmapi.ApiError as e:
        problems.append(f"weather: station lookup failed: {e}"[:300])
    # soonest observation days first, so they get the fresh forecasts
    order = sorted(parsed.items(), key=lambda kv: kv[1][1][1])
    icaos = list(dict.fromkeys(info[2] for _, (_, info) in order))
    fcs = forecasts_for(icaos, coords, fcache, now, fetch, problems)
    today = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")
    picks, notes, rows = [], [], []
    for eid, (ev, (kind, day, icao)) in order:
        fc = fcs.get(icao)
        if not fc or day not in fc["days"] or len(fc["days"][day][kind]) < 20:
            continue
        if day_started(day, fc["offset"], now):
            continue
        lead_h = round((day_start(day, fc["offset"]) - now) / 3600, 1)
        members = fc["days"][day][kind]
        best = None
        bins = []
        for m in ev.get("markets") or []:
            v = views_by_cid.get(m.get("conditionId"))
            rng = parse_range(m.get("groupItemTitle") or "")
            if not v or not rng:
                continue
            lo, hi, unit = rng
            scale = 1.8 if unit == "F" else 1.0
            mu = to_unit(members, unit)
            p = range_prob(mu, lo, hi, SIGMA_C * scale)
            p_raw = range_prob(mu, lo, hi, SIGMA_RAW_C * scale)
            bid, ask = _num(v.get("bestBid")), _num(v.get("bestAsk"))
            bins.append({"range": m.get("groupItemTitle"), "p": round(p, 3), "p_raw": round(p_raw, 3), "bid": bid, "ask": ask})
            sides = []
            if ask is not None:
                sides.append((0, p, p_raw, ask))
            if bid is not None:
                sides.append((1, 1 - p, 1 - p_raw, 1 - bid))
            for idx, prob, prob_raw, price in sides:
                edge, edge_raw = prob - price, prob_raw - price
                if min(prob, prob_raw) >= MIN_PROB and 0 < price <= MAX_PRICE \
                        and edge >= MIN_EDGE and edge_raw >= MIN_EDGE and (best is None or edge > best["edge"]):
                    best = {"view": v, "idx": idx, "edge": edge, "edge_raw": edge_raw, "prob": prob, "prob_raw": prob_raw,
                            "cap": round(min(MAX_PRICE, min(prob, prob_raw) - MIN_EDGE / 2), 3)}
        if bins and logged.get(eid) != today:
            logged[eid] = today
            rows.append({"event_id": eid, "event": ev.get("title"), "station": icao, "kind": kind, "day": day,
                         "lead_h": lead_h, "members": len(members), "mean": round(statistics.fmean(members), 2),
                         "sd": round(statistics.pstdev(members), 2), "bins": bins})
        if best:
            v = best["view"]
            note = {"forecast_chance": round(best["prob"], 3), "forecast_chance_raw": round(best["prob_raw"], 3),
                    "edge": round(best["edge"], 3), "lead_h": lead_h, "station": icao}
            picks.append((v, best["idx"], best["cap"], note))
            notes.append({"event": ev.get("title"), "range": v.get("groupItemTitle"),
                          "side": "Yes" if best["idx"] == 0 else "No", **note})
    for eid in list(logged):
        if eid not in parsed:
            del logged[eid]
    return {"picks": picks, "notes": notes, "rows": rows, "problems": problems}
