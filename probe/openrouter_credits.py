"""Read-only: prints how much OpenRouter credit the account has bought and used
(no key or personal data is printed)."""
import json, os, urllib.error, urllib.request

key = os.environ["OPENROUTER_API_KEY"].strip()
for path in ("/api/v1/credits", "/api/v1/key"):
    req = urllib.request.Request("https://openrouter.ai" + path, headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r).get("data", {})
        keep = {k: d.get(k) for k in ("total_credits", "total_usage", "usage", "limit", "limit_remaining", "is_free_tier") if k in d}
        print(f"== {path}: {keep}", flush=True)
    except urllib.error.HTTPError as e:
        print(f"== {path}: HTTP {e.code}", flush=True)
