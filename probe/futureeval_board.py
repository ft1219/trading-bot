"""Read-only: fetch Metaculus's public FutureEval model leaderboard page and
print the text around the model names we care about."""
import re, urllib.request

NAMES = ["Gemini 3.7 Flash", "Gemini 3.8 Flash", "Sonnet 5.5", "Opus 5.5", "Fable 5.1",
         "Fable 5 ", "Opus 5 ", "DeepSeek V3.2", "Gemini 4 Argon"]
for url in ["https://www.metaculus.com/futureeval/leaderboard/", "https://www.metaculus.com/futureeval/"]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"== {url}: {e!r}", flush=True)
        continue
    text = re.sub(r"\\u0026", "&", html)
    text = re.sub(r'\\"', '"', text)
    print(f"== {url}: {len(html)} chars", flush=True)
    for d in sorted(set(re.findall(r"(?:updated|Updated|as of|As of)[^<\"]{0,60}", text)))[:5]:
        print("   date:", d, flush=True)
    for name in NAMES:
        for m in list(re.finditer(re.escape(name), text))[:3]:
            s = text[max(0, m.start() - 150): m.end() + 250]
            s = re.sub(r"<[^>]+>", " ", s)
            s = re.sub(r"\s+", " ", s)
            print(f"   [{name}] {s}", flush=True)
