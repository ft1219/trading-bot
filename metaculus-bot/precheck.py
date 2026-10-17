"""
Cheap check, run before installing anything: is there an open question in
the tournaments the bot forecasts on that the bot has not forecast yet?

Tournament questions stay open for only 1.5 hours, and the schedule checks
every 40 minutes, so most open questions are seen by two or three runs. The
bot skips questions it already forecast, so those later runs would only spend
GitHub Actions minutes installing it. When there is nothing new, the workflow
skips the slow install and bot steps, which keeps each scheduled run to about
one billed minute.

Standard library only. Any error, or a response shape we do not recognise,
answers "yes, run the bot", so a broken check can cost minutes but never a
missed question.

Usage: python precheck.py [tournament ...]
Writes to_forecast=true|false to $GITHUB_OUTPUT when set, and prints it.
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
PAGE_SIZE = 100


def build_url(tournament: str) -> str:
    query = urllib.parse.urlencode(
        {
            "tournaments": tournament,
            "statuses": "open",
            "limit": PAGE_SIZE,
            # Same as forecasting-tools' own request, which reads
            # question.my_forecasts from this response.
            "with_cp": "true",
        }
    )
    return f"{API_URL}?{query}"


def _questions_in_post(post: dict) -> list[dict]:
    if "group_of_questions" in post:
        return list(post["group_of_questions"]["questions"])
    if "conditional" in post:
        # Mirrors forecasting-tools, which reads question_yes's my_forecasts
        # (question_no's only when question_yes has none at all).
        conditional = post["conditional"]
        yes, no = conditional["question_yes"], conditional["question_no"]
        merged = dict(yes, my_forecasts=yes.get("my_forecasts") or no.get("my_forecasts"))
        return [merged]
    if "question" in post:
        return [post["question"]]
    return []  # notebooks: the bot ignores them too


def _needs_forecast(question: dict) -> bool:
    if question.get("status", "open") != "open":
        return False
    try:
        history = question["my_forecasts"]["history"]
    except (KeyError, TypeError):
        # No forecast data, e.g. the token is missing or wrong: assume new.
        return True
    return not history


def count_to_forecast(payload: dict) -> int:
    results = payload["results"]
    if not isinstance(results, list):
        raise ValueError("unexpected 'results' in API response")
    count = payload.get("count")
    if payload.get("next") or (isinstance(count, int) and count > len(results)):
        # More open posts than one page shows; let the bot sort it out.
        return max(count or 0, len(results) + 1)
    return sum(
        1
        for post in results
        for question in _questions_in_post(post)
        if _needs_forecast(question)
    )


def fetch_json(url: str, token: str | None, timeout: float = 20) -> dict:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    if token:
        request.add_header("Authorization", f"Token {token}")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def has_questions_to_forecast(tournaments, token, fetch=fetch_json) -> bool:
    for tournament in tournaments:
        try:
            waiting = count_to_forecast(fetch(build_url(tournament), token))
        except Exception as e:
            print(f"Pre-check could not read tournament {tournament} ({e!r}); running the bot anyway.")
            return True
        print(f"Tournament {tournament}: {waiting} open question(s) not forecast yet.")
        if waiting > 0:
            return True
    return False


def main(argv: list[str]) -> int:
    tournaments = argv or list(DEFAULT_TOURNAMENTS)
    to_forecast = has_questions_to_forecast(tournaments, os.getenv("METACULUS_TOKEN"))
    line = f"to_forecast={'true' if to_forecast else 'false'}"
    print(line)
    output_path = os.getenv("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
