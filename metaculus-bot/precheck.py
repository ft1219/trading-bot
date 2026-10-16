"""
Cheap check, run before installing anything: are any questions open in the
tournaments the bot forecasts on?

Tournament questions stay open for only 1.5 hours, so "any open question"
means "probably something new to forecast". When nothing is open, the
workflow skips the slow install and bot steps, which keeps each scheduled run
to about one billed GitHub Actions minute.

Standard library only. Any error answers "yes, run the bot", so a broken
check can cost minutes but never a missed question.

Usage: python precheck.py [tournament ...]
Writes has_open=true|false to $GITHUB_OUTPUT when set, and prints it.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

API_URL = "https://www.metaculus.com/api/posts/"
# Must match forecasting_tools.MetaculusClient.CURRENT_AI_COMPETITION_ID and
# CURRENT_MINIBENCH_ID (tests/test_precheck.py checks this).
DEFAULT_TOURNAMENTS = ("33121", "minibench")


def build_url(tournament: str) -> str:
    query = urllib.parse.urlencode(
        {"tournaments": tournament, "statuses": "open", "limit": 1}
    )
    return f"{API_URL}?{query}"


def count_open(payload: dict) -> int:
    results = payload["results"]
    if not isinstance(results, list):
        raise ValueError("unexpected 'results' in API response")
    count = payload.get("count")
    return count if isinstance(count, int) else len(results)


def fetch_json(url: str, token: str | None, timeout: float = 20) -> dict:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    if token:
        request.add_header("Authorization", f"Token {token}")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def has_open_questions(tournaments, token, fetch=fetch_json) -> bool:
    for tournament in tournaments:
        try:
            if count_open(fetch(build_url(tournament), token)) > 0:
                return True
        except Exception as e:
            print(f"Pre-check could not read tournament {tournament} ({e}); running the bot anyway.")
            return True
    return False


def main(argv: list[str]) -> int:
    tournaments = argv or list(DEFAULT_TOURNAMENTS)
    has_open = has_open_questions(tournaments, os.getenv("METACULUS_TOKEN"))
    line = f"has_open={'true' if has_open else 'false'}"
    print(line)
    output_path = os.getenv("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
