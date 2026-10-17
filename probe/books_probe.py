"""
One-off: raw books and market fields for the practice watchlist, to check
why most watched markets show no competing orders. Read-only, public data.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
CLOB = "https://clob.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com"


def get(url, data=None):
    headers = {"Accept": "application/json", "User-Agent": "trading-bot-probe/0.1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=25) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": repr(e)}


watch = json.load(open(os.path.join(os.path.dirname(__file__), "watch.json")))
now = int(time.time())
summary = []
batch = get(f"{CLOB}/books", [{"token_id": w["yes"]} for w in watch])
batch_by = {b.get("asset_id"): b for b in batch} if isinstance(batch, list) else {}
for w in sorted(watch, key=lambda w: w["rank"]):
    single = get(f"{CLOB}/book?token_id={w['yes']}")
    single_no = get(f"{CLOB}/book?token_id={w['no']}")
    gm = get(f"{GAMMA}/markets?condition_ids={w['cid']}")
    gm = gm[0] if isinstance(gm, list) and gm else gm
    trades = get(f"{DATA}/trades?market={w['cid']}&limit=500&takerOnly=false")
    t24 = [t for t in trades if isinstance(t, dict) and t.get("timestamp", 0) >= now - 86400] if isinstance(trades, list) else []
    with open(os.path.join(OUT, f"rank{w['rank']:02d}.json"), "w") as f:
        json.dump({"watch": w, "book_single": single, "book_no": single_no, "book_batch": batch_by.get(w["yes"]),
                   "gamma": gm, "trades_24h": t24[:50]}, f, indent=1)

    def top(book, side, n=6):
        lv = (book or {}).get(side) or []
        lv = sorted(lv, key=lambda x: float(x["price"]), reverse=(side == "bids"))
        return [(x["price"], x["size"]) for x in lv[:n]]

    row = {
        "rank": w["rank"],
        "q": (gm or {}).get("question", "")[:60] if isinstance(gm, dict) else "",
        "single_bids": top(single, "bids"), "single_asks": top(single, "asks"),
        "batch_bids": top(batch_by.get(w["yes"]), "bids"), "batch_asks": top(batch_by.get(w["yes"]), "asks"),
        "no_bids": top(single_no, "bids", 3), "no_asks": top(single_no, "asks", 3),
        "n_levels": [len((single or {}).get("bids") or []), len((single or {}).get("asks") or [])],
        "gamma": {k: (gm or {}).get(k) for k in ("bestBid", "bestAsk", "spread", "lastTradePrice", "liquidityClob",
                                                  "volume24hrClob", "rewardsMinSize", "rewardsMaxSpread", "competitive",
                                                  "clobRewards", "createdAt", "startDate")} if isinstance(gm, dict) else gm,
        "trades_24h": len(t24),
    }
    summary.append(row)
    print(json.dumps(row))
with open(os.path.join(OUT, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
