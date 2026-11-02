"""Read-only: makes one small AskNews call (about 1 credit) and prints what the
API reports back: status, per-call credit use and any header about limits or
credits. Never prints the key."""
import json, os, urllib.error, urllib.parse, urllib.request

KEY = os.environ["ASKNEWS_API_KEY"].strip()
params = {"query": "Metaculus forecasting", "n_articles": 1, "return_type": "string", "strategy": "latest news"}
url = "https://api.asknews.app/v1/news/search?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}", "Accept": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        status, headers, body = r.status, dict(r.headers.items()), r.read()
except urllib.error.HTTPError as e:
    status, headers, body = e.code, dict(e.headers.items()), e.read()
print("HTTP", status, flush=True)
for k, v in sorted(headers.items()):
    if k.lower() in ("set-cookie", "authorization"):
        continue
    print(f"header {k}: {v}", flush=True)
try:
    data = json.loads(body or b"null")
except Exception:
    data = None
if isinstance(data, dict):
    print("body keys:", sorted(data.keys()), flush=True)
    for k in ("usage", "hit_cache", "code", "detail", "status_code"):
        if k in data:
            print(f"{k}: {json.dumps(data[k])[:300]}", flush=True)
else:
    print("body:", (body or b"")[:300].decode(errors="replace"), flush=True)
