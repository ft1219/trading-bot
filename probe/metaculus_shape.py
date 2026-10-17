"""Prints the paging fields and shape (not the content) of open tournament posts, to check precheck.py."""
import json, os, urllib.request, sys
sys.path.insert(0, "metaculus-bot")
import precheck
token = os.environ.get("METACULUS_TOKEN")


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "Authorization": f"Token {token}"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


for t in precheck.DEFAULT_TOURNAMENTS:
    url = precheck.build_url(t)
    body = get(url)
    res = body.get("results", [])
    print(f"== {t}: url={url}")
    print(f"   top-level keys={sorted(body.keys())} count={body.get('count')!r} next={body.get('next')!r} previous={body.get('previous')!r} results={len(res)}")
    try:
        print(f"   count_to_forecast={precheck.count_to_forecast(body)}")
    except Exception as e:
        print(f"   count_to_forecast raised {e!r}")
    for post in res:
        qs = precheck._questions_in_post(post)
        print("   post", post.get("id"), "status", post.get("status"), "kind", [k for k in ("question", "group_of_questions", "conditional") if k in post],
              "keys" if not qs else "", sorted(post.keys()) if not qs else "", {k: post.get(k) for k in ("type", "curation_status", "open_time", "scheduled_close_time")} if not qs else "",
              "questions", [(q.get("id"), q.get("status"), type(q.get("my_forecasts")).__name__,
                             len(((q.get("my_forecasts") or {}).get("history")) or []), precheck._needs_forecast(q)) for q in qs])
    if body.get("next"):
        nxt = get(body["next"])
        print(f"   NEXT PAGE: count={nxt.get('count')!r} next={nxt.get('next')!r} results={len(nxt.get('results', []))} ids={[p.get('id') for p in nxt.get('results', [])][:10]}")
    # same query with a small page, to see how count/next behave
    small = get(url.replace("limit=100", "limit=1"))
    print(f"   limit=1: count={small.get('count')!r} next={small.get('next')!r} results={len(small.get('results', []))}")

print("== precheck says:")
sys.argv = ["precheck.py"]
precheck.main([])
