"""Read-only: prints the bot's resolved questions with their scores, and the
tournament leaderboards (our rank and Metaculus's own baseline bots)."""
import json, os, sys, time, urllib.error, urllib.request
from collections import Counter, defaultdict

sys.path.insert(0, "metaculus-bot")
import precheck

TOKEN = os.environ["METACULUS_TOKEN"]
BASE = "https://www.metaculus.com/api"


def get(path):
    # Metaculus's Cloudflare rate-limits fast callers (error 1015), so go slowly.
    url = path if path.startswith("http") else BASE + path
    for attempt in range(5):
        time.sleep(4)
        req = urllib.request.Request(url, headers={"Accept": "application/json", "Authorization": f"Token {TOKEN}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(30 * (attempt + 1))
                continue
            return e.code, e.read()[:200].decode(errors="replace")
        except Exception as e:
            return None, repr(e)[:200]
    return 429, "still rate limited"


status, me = get("/users/me")
uid, uname = me.get("id"), me.get("username")
print(f"== me: id={uid} username={uname} status={status}")

# Every post the bot has forecast, any status.
posts, url = [], f"/posts/?forecaster_id={uid}&limit=100&with_cp=true"
while url and len(posts) < 1000:
    status, body = get(url)
    if status != 200:
        print("posts error", status, body)
        break
    posts += body.get("results", [])
    url = body.get("next")
print(f"== posts forecast by the bot: {len(posts)}")

shown = 0
by_project = defaultdict(list)
for post in posts:
    proj = post.get("projects") or {}
    if shown == 0:
        print("   sample projects:", json.dumps({k: [(x.get("id"), x.get("slug"), x.get("type")) for x in v] if isinstance(v, list) else v for k, v in proj.items()})[:600])
    tours = ([(t.get("id"), t.get("slug")) for t in (proj.get("tournament") or [])]
             or [(t.get("id"), t.get("slug")) for t in (proj.get("question_series") or [])]
             or [((post.get("default_project") or {}).get("id"), (post.get("default_project") or {}).get("slug"))])
    for q in precheck._questions_in_post(post):
        mf = q.get("my_forecasts") or {}
        if shown < 2 and q.get("status") == "resolved":
            print("   sample my_forecasts keys:", sorted(mf.keys()), "score_data:", json.dumps(mf.get("score_data"))[:600])
            print("   sample question keys:", sorted(q.keys()))
            shown += 1
        by_project[tours[0]].append((post, q, mf))

for (tid, slug), items in sorted(by_project.items(), key=lambda x: str(x[0])):
    st = Counter(q.get("status") for _, q, _ in items)
    print(f"\n== tournament id={tid} slug={slug}: {len(items)} question(s), statuses={dict(st)}")
    sums = defaultdict(float)
    n = 0
    for post, q, mf in items:
        if q.get("status") != "resolved":
            continue
        sd = mf.get("score_data") or {}
        latest = mf.get("latest") or {}
        fv = latest.get("forecast_values")
        mine = fv[1] if q.get("type") == "binary" and isinstance(fv, list) and len(fv) == 2 else None
        n += 1
        for k, v in sd.items():
            if isinstance(v, (int, float)):
                sums[k] += v
        print(f"   q{q.get('id')} {q.get('type')} res={q.get('resolution')} mine={mine} "
              f"scores={ {k: round(v, 2) for k, v in sd.items() if isinstance(v, (int, float))} } | {(post.get('title') or '')[:70]}")
    if n:
        print(f"   RESOLVED {n}: totals={ {k: round(v, 2) for k, v in sums.items()} } means={ {k: round(v / n, 2) for k, v in sums.items()} }")

# Leaderboards: try the endpoints the website uses.
tids = {t for t, _ in by_project if isinstance(t, int)} | {33121}
for tid in sorted(tids, key=str):
    for path in (f"/leaderboards/project/{tid}/", f"/leaderboards/project/{tid}/?primary=true", f"/projects/{tid}/leaderboard/"):
        status, body = get(path)
        if status != 200 or not isinstance(body, dict):
            print(f"\n== leaderboard {path}: HTTP {status} {str(body)[:120]}")
            continue
        entries = body.get("entries") or body.get("results") or []
        print(f"\n== leaderboard {path}: keys={sorted(body.keys())} entries={len(entries)} "
              f"name={body.get('name')!r} score_type={body.get('score_type')!r} finalized={body.get('finalized')!r}")
        def row(e):
            u = e.get("user") or {}
            return (f"rank={e.get('rank')} score={round(e.get('score') or 0, 2)} take={round(e.get('take') or 0, 3)} "
                    f"prize={e.get('prize')} questions={e.get('contribution_count')} user={u.get('username') or e.get('aggregation_method')} bot={u.get('is_bot')}")
        for e in entries[:8]:
            print("   top", row(e))
        for e in entries:
            u = e.get("user") or {}
            if u.get("id") == uid or u.get("username") == uname:
                print("   >>> OURS", row(e))
        for e in entries:
            name = ((e.get("user") or {}).get("username") or "")
            if name.lower().startswith("metac-"):
                print("   metac", row(e))
        me_entry = body.get("userEntry") or body.get("user_entry")
        if me_entry:
            print("   user_entry", row(me_entry))
        break
