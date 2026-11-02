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
for slug in ("33121", "minibench", "bot-testing-area"):
    url = f"{BASE}/posts/?tournaments={slug}&forecaster_id={uid}&limit=100&order_by=-published_at"
    n, months, statuses, pages = 0, Counter(), Counter(), 0
    while url and pages < 6:
        status, body = get(url)
        pages += 1
        if status != 200 or not isinstance(body, dict):
            print(f"{slug}: HTTP {status} {str(body)[:120]}", flush=True)
            break
        for post in body.get("results", []):
            n += 1
            q = post.get("question") or {}
            statuses[q.get("status") or post.get("status")] += 1
            months[(post.get("published_at") or post.get("open_time") or "")[:10]] += 1
        url = body.get("next")
    print(f"== {slug}: {n} question(s) forecast; statuses={dict(statuses)}", flush=True)
    print("   by publish date:", dict(sorted(months.items())), flush=True)
