"""Read-only: counts the questions the bot account has forecast, per tournament,
to estimate how many AskNews lookups the bot has made. Few, slow requests."""
import json, os, time, urllib.error, urllib.request
from collections import Counter

TOKEN = os.environ["METACULUS_TOKEN"]
BASE = "https://www.metaculus.com/api"


def get(url):
    for _ in range(3):
        time.sleep(8)
        req = urllib.request.Request(url, headers={"Accept": "application/json", "Authorization": f"Token {TOKEN}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(60)
                continue
            return e.code, e.read()[:200].decode(errors="replace")
        except Exception as e:
            return None, repr(e)[:200]
    return 429, "still rate limited"


status, me = get(BASE + "/users/me")
uid = me["id"]
url = f"{BASE}/posts/?forecaster_id={uid}&limit=100&order_by=-published_at"
n, groups, pages = 0, Counter(), 0
while url and pages < 8:
    status, body = get(url)
    pages += 1
    if status != 200 or not isinstance(body, dict):
        print(f"all: HTTP {status} {str(body)[:120]}", flush=True)
        break
    for post in body.get("results", []):
        n += 1
        tours = (post.get("projects") or {}).get("tournament") or []
        name = ",".join(f"{t.get('id')}:{t.get('slug')}" for t in tours) or "none"
        groups[(name, (post.get("published_at") or "")[:7])] += 1
    url = body.get("next")
print(f"== all: {n} question(s) forecast over {pages} page(s)", flush=True)
for (name, month), c in sorted(groups.items()):
    print(f"   {name} {month}: {c}", flush=True)
