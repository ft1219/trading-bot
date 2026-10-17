"""
One-off, read-only check before Data API v1 retires (2026-10-24): does
/v2/trades?taker_only=false return the same taker and maker rows as
v1 /trades?takerOnly=false, in what order, with what types, and with how much
lag? Also compares /v2/prices-history with the CLOB /prices-history route.
Public endpoints only; no keys.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "trading-bot-shadow-probe/0.1 (read-only)"
DATA = "https://data-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
WINDOW = 7200
SETTLE = 300


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                hdrs = {k.lower(): v for k, v in r.headers.items()}
                return r.status, hdrs, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            return e.code, {k.lower(): v for k, v in e.headers.items()}, {"_error": body}
        except Exception as e:
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            return -1, {}, {"_error": repr(e)}


def interesting_headers(h):
    return {k: v for k, v in h.items() if k in ("deprecation", "sunset", "warning", "link", "x-deprecated", "retry-after")}


def v1_rows(cid, since):
    rows, offset, pages = [], 0, 0
    hdr = {}
    while offset <= 3000:
        st, h, page = get(f"{DATA}/trades?market={cid}&takerOnly=false&limit=500&offset={offset}")
        pages += 1
        hdr = hdr or interesting_headers(h)
        if st != 200 or not isinstance(page, list):
            return rows, {"status": st, "error": page, "pages": pages, "headers": hdr}
        rows += page
        if len(page) < 500 or int(page[-1]["timestamp"]) <= since:
            break
        offset += 500
    return rows, {"status": 200, "pages": pages, "headers": hdr}


def v2_rows(cid, since, taker_only="false", limit=1000, max_pages=30):
    rows, pages, cursor = [], 0, None
    meta = {"pages": 0, "has_more_last": None, "page_sizes": [], "limits": []}
    while pages < max_pages:
        q = {"condition": cid, "taker_only": taker_only, "limit": limit}
        if cursor:
            q["cursor"] = cursor
        st, h, body = get(f"{DATA}/v2/trades?" + urllib.parse.urlencode(q))
        pages += 1
        meta["pages"] = pages
        meta.setdefault("headers", interesting_headers(h))
        if st != 200 or not isinstance(body, dict):
            meta.update(status=st, error=body)
            return rows, meta
        data = body.get("data") or []
        pg = body.get("pagination") or {}
        meta["page_sizes"].append(len(data))
        meta["limits"].append(pg.get("limit"))
        meta["has_more_last"] = pg.get("has_more")
        rows += data
        cursor = pg.get("next_cursor")
        if not cursor or not data or int(data[-1]["timestamp"]) <= since:
            break
    meta["status"] = 200
    meta["hit_page_cap"] = pages >= max_pages
    return rows, meta


def key_v1(r):
    return (r.get("transactionHash"), str(r.get("asset")), r.get("side"), round(float(r["size"]), 6),
            round(float(r["price"]), 6), int(r["timestamp"]), (r.get("proxyWallet") or "").lower())


def key_v2(r):
    return (r.get("transaction_hash"), str(r.get("token_id")), r.get("side"), round(float(r["size"]), 6),
            round(float(r["price"]), 6), int(r["timestamp"]), (r.get("proxy_wallet") or "").lower())


def multiset(keys):
    out = {}
    for k in keys:
        out[k] = out.get(k, 0) + 1
    return out


def diff(a, b):
    only = []
    for k, n in a.items():
        if n > b.get(k, 0):
            only.append((k, n - b.get(k, 0)))
    return only


def order_check(rows):
    ts = [int(r["timestamp"]) for r in rows]
    return {"nonincreasing": all(x >= y for x, y in zip(ts, ts[1:])),
            "nondecreasing": all(x <= y for x, y in zip(ts, ts[1:]))}


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    markets = json.load(open(os.path.join(os.path.dirname(__file__), "markets_v2.json")))
    now = int(time.time())
    since = now - WINDOW
    report = {"now": now, "window_s": WINDOW, "settle_s": SETTLE, "markets": []}
    best = None
    for m in markets:
        cid = m["condition_id"]
        r1, meta1 = v1_rows(cid, since)
        r2, meta2 = v2_rows(cid, since)
        r2t, meta2t = v2_rows(cid, since, taker_only="true", max_pages=5)
        lo, hi = since, now - SETTLE
        w1 = [r for r in r1 if lo < int(r["timestamp"]) <= hi]
        w2 = [r for r in r2 if lo < int(r["timestamp"]) <= hi]
        w2t = [r for r in r2t if lo < int(r["timestamp"]) <= hi]
        m1, m2 = multiset(map(key_v1, w1)), multiset(map(key_v2, w2))
        only1, only2 = diff(m1, m2), diff(m2, m1)
        # looser match ignoring wallet and price rounding
        loose = lambda k: (k[0], k[1], k[2], round(k[3], 2), k[5])
        l1, l2 = multiset(loose(k) for k in map(key_v1, w1)), multiset(loose(k) for k in map(key_v2, w2))
        tx_v1 = {r.get("transactionHash") for r in w1}
        tx_v2t = {r.get("transaction_hash") for r in w2t}
        entry = {
            "condition_id": cid, "rank": m["rank"], "pilot": m["pilot"],
            "v1": dict(meta1, rows=len(r1), in_window=len(w1), newest=max([int(r["timestamp"]) for r in r1], default=None),
                       order=order_check(r1)),
            "v2": dict(meta2, rows=len(r2), in_window=len(w2), newest=max([int(r["timestamp"]) for r in r2], default=None),
                       order=order_check(r2)),
            "v2_taker_only": dict(meta2t, rows=len(r2t), in_window=len(w2t)),
            "only_in_v1": len(only1), "only_in_v2": len(only2),
            "only_in_v1_examples": [list(k) + [n] for k, n in only1[:4]],
            "only_in_v2_examples": [list(k) + [n] for k, n in only2[:4]],
            "loose_only_v1": len(diff(l1, l2)), "loose_only_v2": len(diff(l2, l1)),
            "tx_v1": len(tx_v1), "tx_v2_taker_only": len(tx_v2t), "tx_v1_not_in_v2_taker": len(tx_v1 - tx_v2t),
            "v2_field_types": {k: type(v).__name__ for k, v in (r2[0].items() if r2 else [])},
            "v2_tokens_seen": sorted({str(r.get("token_id")) == m["yes_token"] for r in r2}),
            "v2_outcome_index": sorted({r.get("outcome_index") for r in r2}),
        }
        report["markets"].append(entry)
        if w2 and (best is None or len(w2) > best[0]):
            best = (len(w2), m, w1, w2, r2[:2])
        time.sleep(0.2)

    if best:
        _, m, w1, w2, raw2 = best
        keep = ("proxy_wallet", "side", "token_id", "condition_id", "size", "price", "timestamp",
                "outcome", "outcome_index", "transaction_hash")
        json.dump({"market": m, "window": [since, now - SETTLE], "raw_first_rows": raw2,
                   "v2_rows": [{k: r.get(k) for k in keep} for r in w2],
                   "v1_rows": w1}, open(os.path.join(out_dir, "trades_v1_v2_sample.json"), "w"), indent=1)

    # prices-history: CLOB route vs /v2/prices-history for the top two markets
    ph = []
    for m in markets[:3]:
        tok = m["yes_token"]
        st1, h1, b1 = get(f"{CLOB}/prices-history?market={tok}&startTs={since}&endTs={now}&fidelity=1")
        st2, h2, b2 = get(f"{DATA}/v2/prices-history?" + urllib.parse.urlencode({"token_id": tok, "start": since, "end": now, "bucket_seconds": 60}))
        p1 = {int(p["t"]): float(p["p"]) for p in (b1.get("history") or [])} if isinstance(b1, dict) else {}
        p2 = {int(p["timestamp"]): float(p["price"]) for p in (b2.get("data") or [])} if isinstance(b2, dict) else {}
        common = sorted(set(p1) & set(p2))
        diffs = [abs(p1[t] - p2[t]) for t in common]
        ph.append({"token": tok[:12], "clob_status": st1, "clob_headers": interesting_headers(h1), "clob_points": len(p1),
                   "v2_status": st2, "v2_points": len(p2), "v2_pagination": (b2.get("pagination") if isinstance(b2, dict) else None),
                   "common_ts": len(common), "max_abs_diff": max(diffs, default=None),
                   "n_diff_gt_0.001": sum(d > 0.001 for d in diffs),
                   "clob_first_last": [min(p1, default=None), max(p1, default=None)],
                   "v2_first_last": [min(p2, default=None), max(p2, default=None)],
                   "v2_sample": (b2.get("data") or [])[:3] if isinstance(b2, dict) else b2,
                   "v2_resolution": sorted({p.get("resolution_seconds") for p in (b2.get("data") or [])}) if isinstance(b2, dict) else None})
    report["prices_history"] = ph
    json.dump(report, open(os.path.join(out_dir, "trades_v2_report.json"), "w"), indent=1)
    s = {"markets": len(report["markets"]),
         "all_equal": sum(1 for e in report["markets"] if e["only_in_v1"] == 0 and e["only_in_v2"] == 0),
         "rows_v1": sum(e["v1"]["in_window"] for e in report["markets"]),
         "rows_v2": sum(e["v2"]["in_window"] for e in report["markets"])}
    print(json.dumps(s))
    for e in report["markets"]:
        print(e["rank"], e["condition_id"][:10], "v1", e["v1"]["in_window"], "v2", e["v2"]["in_window"],
              "only1", e["only_in_v1"], "only2", e["only_in_v2"], "loose", e["loose_only_v1"], e["loose_only_v2"],
              "order2", e["v2"]["order"], "newest", e["v1"]["newest"], e["v2"]["newest"], "pages", e["v2"]["pages"])
    for p in ph:
        print(json.dumps(p)[:600])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
