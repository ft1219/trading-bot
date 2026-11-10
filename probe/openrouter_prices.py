"""Read-only: prints OpenRouter's public price list for the models we use or
might switch to. No key needed."""
import json, urllib.request

WANT = ("gemini-3.7-flash", "gemini-3.8-flash", "claude-sonnet-5", "claude-opus-5",
        "claude-fable", "deepseek-v3.2", "deepseek-v4", "gemini-4")
req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"Accept": "application/json"})
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.load(r)["data"]
print(f"== {len(data)} models listed", flush=True)
for m in sorted(data, key=lambda m: m["id"]):
    if any(w in m["id"] for w in WANT):
        p = m.get("pricing") or {}
        per_m = lambda k: round(float(p.get(k) or 0) * 1e6, 4)
        print(f"   {m['id']}: in ${per_m('prompt')}/M out ${per_m('completion')}/M "
              f"reasoning ${per_m('internal_reasoning')}/M expires={m.get('expiration_date')} "
              f"params={'reasoning' in (m.get('supported_parameters') or [])}", flush=True)
