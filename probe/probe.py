"""
One-off live probe of Polymarket's public read-only API, run on GitHub
Actions (this repo's build sandbox cannot reach Polymarket). Saves raw
responses and a summary so the practice recorder can be built against the
real shapes. Read-only: no keys, no account, no orders.
"""
import concurrent.futures as cf
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
CLOB = "https://clob.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com"
MAX_BODY = 3_000_000


def fetch(url, data=None, timeout=25):
    headers = {"Accept": "application/json", "User-Agent": "trading-bot-probe/0.1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, raw, hdrs = r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        status, raw, hdrs = e.code, e.read(), dict(e.headers)
    except Exception as e:  # network errors are data here
        return {"url": url, "error": repr(e), "elapsed_s": round(time.time() - t0, 3)}
    try:
        body = json.loads(raw)
    except Exception:
        body = raw[:20000].decode("utf-8", "replace")
    keep = {k: v for k, v in hdrs.items() if k.lower().startswith(("x-ratelimit", "retry-after", "cf-", "server", "content-type", "age", "cache"))}
    return {"url": url, "status": status, "elapsed_s": round(time.time() - t0, 3), "bytes": len(raw), "headers": keep, "body": body}


def save(name, result):
    text = json.dumps(result, indent=1)
    if len(text) > MAX_BODY:
        body = result.get("body")
        if isinstance(body, dict) and isinstance(body.get("data"), list):
            result = dict(result, body=dict(body, data=body["data"][:40]), truncated=True)
        elif isinstance(body, list):
            result = dict(result, body=body[:200], truncated=True)
        text = json.dumps(result, indent=1)[:MAX_BODY]
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        f.write(text)
    status = result.get("status", result.get("error"))
    print(f"{name}: {status} {result.get('elapsed_s')}s {result.get('bytes', 0)}B")


start = time.time()
simple = {
    "geoblock": "https://polymarket.com/api/geoblock",
    "clob_time": f"{CLOB}/time",
    "clob_ok": f"{CLOB}/ok",
    "sampling_markets_p1": f"{CLOB}/sampling-markets",
    "sampling_simplified_p1": f"{CLOB}/sampling-simplified-markets",
    "rewards_markets_current": f"{CLOB}/rewards/markets/current",
    "rewards_markets": f"{CLOB}/rewards/markets",
    "rewards_markets_multi": f"{CLOB}/rewards/markets/multi",
    "gamma_markets_top": f"{GAMMA}/markets?active=true&closed=false&limit=50&order=volume24hr&ascending=false",
    "gamma_events_top": f"{GAMMA}/events?active=true&closed=false&limit=5&order=volume24hr&ascending=false",
    "data_trades_recent": f"{DATA}/trades?limit=5",
    "rebates_current": f"{CLOB}/rebates/current",
}
with cf.ThreadPoolExecutor(8) as ex:
    for name, res in zip(simple, ex.map(fetch, simple.values())):
        save(name, res)

# Walk every page of reward-eligible markets.
markets, cursor, pages = [], "", 0
while pages < 60:
    res = fetch(f"{CLOB}/sampling-markets" + (f"?next_cursor={urllib.parse.quote(cursor)}" if cursor else ""))
    pages += 1
    body = res.get("body")
    if not isinstance(body, dict) or "data" not in body:
        save(f"sampling_markets_error_p{pages}", res)
        break
    markets.extend(body["data"])
    cursor = body.get("next_cursor") or ""
    if not cursor or cursor == "LTE=":
        break
print(f"sampling-markets: {len(markets)} markets over {pages} pages in {time.time() - start:.1f}s")


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


rows = []
for m in markets:
    rw = m.get("rewards") or {}
    rates = rw.get("rates") or []
    daily = sum(num(r.get("rewards_daily_rate")) or 0 for r in rates)
    toks = m.get("tokens") or []
    prices = [num(t.get("price")) for t in toks]
    rows.append({
        "condition_id": m.get("condition_id"),
        "question": (m.get("question") or "")[:90],
        "active": m.get("active"), "closed": m.get("closed"),
        "accepting_orders": m.get("accepting_orders"),
        "end_date_iso": m.get("end_date_iso"),
        "neg_risk": m.get("neg_risk"),
        "min_size": num(rw.get("min_size")), "max_spread": num(rw.get("max_spread")),
        "daily_rate": daily, "n_rates": len(rates),
        "price0": prices[0] if prices else None,
        "minimum_order_size": m.get("minimum_order_size"), "minimum_tick_size": m.get("minimum_tick_size"),
        "tokens": [t.get("token_id") for t in toks],
        "keys": sorted(m.keys()),
    })


def dist(values):
    v = sorted(x for x in values if x is not None)
    if not v:
        return {}
    q = lambda p: v[min(len(v) - 1, int(p * len(v)))]
    return {"n": len(v), "min": v[0], "p10": q(.1), "p50": q(.5), "p90": q(.9), "max": v[-1], "sum": round(sum(v), 2)}


live = [r for r in rows if r["accepting_orders"] and not r["closed"]]
mid_ok = [r for r in live if r["price0"] is not None and 0.15 <= r["price0"] <= 0.85]
summary = {
    "total_sampling_markets": len(rows), "accepting_orders": len(live), "mid_0.15_0.85": len(mid_ok),
    "min_size": dist(r["min_size"] for r in live), "max_spread": dist(r["max_spread"] for r in live),
    "daily_rate": dist(r["daily_rate"] for r in live),
    "min_size_counts": {str(k): sum(1 for r in live if r["min_size"] == k) for k in sorted({r["min_size"] for r in live if r["min_size"] is not None})},
    "market_keys": rows[0]["keys"] if rows else [],
    "top_by_daily_rate": sorted(mid_ok, key=lambda r: -r["daily_rate"])[:40],
    "cheapest_min_size_with_rewards": sorted([r for r in mid_ok if r["daily_rate"] > 0], key=lambda r: (r["min_size"] or 1e9, -r["daily_rate"]))[:40],
}
with open(os.path.join(OUT, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
with open(os.path.join(OUT, "sampling_markets_rows.json"), "w") as f:
    json.dump(rows, f)
print(json.dumps({k: summary[k] for k in ("total_sampling_markets", "accepting_orders", "mid_0.15_0.85", "min_size", "max_spread", "daily_rate", "min_size_counts")}, indent=1))

# Deep-dive a few reward markets: books, history, trades, fees.
picks = (summary["cheapest_min_size_with_rewards"][:2] + summary["top_by_daily_rate"][:2])
seen = set()
now = int(time.time())
for i, r in enumerate(picks):
    if r["condition_id"] in seen or not r["tokens"]:
        continue
    seen.add(r["condition_id"])
    t0, cid = r["tokens"][0], r["condition_id"]
    calls = {
        f"m{i}_book_t0": (f"{CLOB}/book?token_id={t0}", None),
        f"m{i}_book_t1": (f"{CLOB}/book?token_id={r['tokens'][-1]}", None),
        f"m{i}_books_batch": (f"{CLOB}/books", [{"token_id": t} for t in r["tokens"]]),
        f"m{i}_midpoint": (f"{CLOB}/midpoint?token_id={t0}", None),
        f"m{i}_spread": (f"{CLOB}/spread?token_id={t0}", None),
        f"m{i}_tick_size": (f"{CLOB}/tick-size?token_id={t0}", None),
        f"m{i}_neg_risk": (f"{CLOB}/neg-risk?token_id={t0}", None),
        f"m{i}_fee_rate": (f"{CLOB}/fee-rate?token_id={t0}", None),
        f"m{i}_fee_rate_bps": (f"{CLOB}/fee-rate-bps?token_id={t0}", None),
        f"m{i}_hist_1d_f1": (f"{CLOB}/prices-history?market={t0}&interval=1d&fidelity=1", None),
        f"m{i}_hist_6h_ts": (f"{CLOB}/prices-history?market={t0}&startTs={now - 6 * 3600}&endTs={now}&fidelity=1", None),
        f"m{i}_hist_max_f60": (f"{CLOB}/prices-history?market={t0}&interval=max&fidelity=60", None),
        f"m{i}_trades_500": (f"{DATA}/trades?market={cid}&limit=500", None),
        f"m{i}_trades_all_types": (f"{DATA}/trades?market={cid}&limit=500&takerOnly=false", None),
        f"m{i}_trades_offset": (f"{DATA}/trades?market={cid}&limit=100&offset=500", None),
        f"m{i}_gamma_market": (f"{GAMMA}/markets?condition_ids={cid}", None),
        f"m{i}_clob_market": (f"{CLOB}/markets/{cid}", None),
    }
    with cf.ThreadPoolExecutor(8) as ex:
        futs = {name: ex.submit(fetch, url, data) for name, (url, data) in calls.items()}
        for name, fut in futs.items():
            save(name, fut.result())

# Rate-limit feel: 30 quick book requests in parallel.
if picks:
    t = time.time()
    with cf.ThreadPoolExecutor(10) as ex:
        res = list(ex.map(lambda _: fetch(f"{CLOB}/book?token_id={picks[0]['tokens'][0]}"), range(30)))
    save("burst_30_books", {"elapsed_s": round(time.time() - t, 3), "statuses": [x.get("status", x.get("error")) for x in res], "headers_last": res[-1].get("headers")})
print(f"total probe time {time.time() - start:.1f}s")
