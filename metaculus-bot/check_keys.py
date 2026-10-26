"""
Checks the keys saved as GitHub secrets, without printing them.

Run it from the Actions tab ("Check my keys"). It tells you, in plain words,
which keys are missing, which ones the services accept, and whether the
OpenRouter key has a spending limit. Standard library only.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import bot_config
import precheck

OK, BAD, UNSURE = "OK", "PROBLEM", "COULD NOT CONFIRM"


def http(url: str, headers: dict, data: bytes | None = None, timeout: float = 20):
    request = urllib.request.Request(url, data=data, headers={"Accept": "application/json", **headers})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, repr(e)


def check_metaculus(token: str | None, get=None) -> tuple[str, str]:
    get = get or http
    if not token:
        return BAD, "METACULUS_TOKEN is missing."
    status, body = get("https://www.metaculus.com/api/users/me", {"Authorization": f"Token {token}"})
    if status in (401, 403):
        return BAD, "Metaculus does not accept METACULUS_TOKEN. Copy the bot's token again."
    if status != 200 or not isinstance(body, dict):
        return UNSURE, f"Metaculus did not answer normally (HTTP {status}). Try again later."
    name = body.get("username", "?")
    if body.get("is_bot") is False:
        return BAD, (
            f"METACULUS_TOKEN works, but it belongs to '{name}', which is not a bot account. "
            "Create a bot under Settings > My Forecasting Bots and use the bot's token."
        )
    return OK, f"METACULUS_TOKEN works for the account '{name}'."


def check_forecast_data(token: str | None, get=None) -> tuple[str, str]:
    """
    Confirms the open-question check can see the bot's own forecasts. Without
    them it cannot tell which questions are done, so every scheduled run
    installs and starts the bot while any question is open.
    """
    get = get or http
    if not token:
        return UNSURE, "Skipped the open-question check because METACULUS_TOKEN is missing."
    parts, questions, visible = [], 0, 0
    for tournament in precheck.DEFAULT_TOURNAMENTS:
        status, body = get(precheck.build_url(tournament), {"Authorization": f"Token {token}"})
        if status != 200 or not isinstance(body, dict) or not isinstance(body.get("results"), list):
            return UNSURE, f"Could not list open questions in {tournament} (HTTP {status})."
        try:
            qs = [q for post in body["results"] for q in precheck._questions_in_post(post)]
            waiting = precheck.count_to_forecast(body)
        except Exception as e:
            return UNSURE, (f"Could not read the open questions in {tournament} ({type(e).__name__}); "
                            "the scheduled run will still forecast.")
        questions += len(qs)
        visible += sum(1 for q in qs if isinstance(q.get("my_forecasts"), dict)
                       and isinstance(q["my_forecasts"].get("history"), list))
        if precheck.page_is_full(body):
            parts.append(f"{tournament}: more than {len(qs)} open questions")
        else:
            parts.append(f"{tournament}: {len(qs)} open question(s), {waiting} not forecast yet")
    if questions and not visible:
        return UNSURE, ("Open questions: " + "; ".join(parts) + ". Metaculus did not show the bot's own forecasts, "
                        "so scheduled runs cannot skip questions it already answered (this costs GitHub minutes, not money).")
    return OK, "Open questions: " + "; ".join(parts) + "."


def check_openrouter(key: str | None, get=None) -> tuple[str, str]:
    get = get or http
    if not key:
        return BAD, "OPENROUTER_API_KEY is missing."
    for url in ("https://openrouter.ai/api/v1/key", "https://openrouter.ai/api/v1/auth/key"):
        status, body = get(url, {"Authorization": f"Bearer {key}"})
        if status == 200 and isinstance(body, dict):
            data = body.get("data") or {}
            limit, usage = data.get("limit"), data.get("usage") or 0
            if limit is None:
                return BAD, (
                    "OPENROUTER_API_KEY works but has no spending limit. "
                    "Set a $40-60 limit on the key in OpenRouter."
                )
            if data.get("limit_reset"):
                return BAD, (
                    f"OPENROUTER_API_KEY's ${limit:.2f} limit starts again every {data['limit_reset']}, so it does not "
                    "cap the whole season. Edit the key in OpenRouter and set the limit reset to none."
                )
            remaining = data.get("limit_remaining")
            if usage >= limit or (remaining is not None and remaining <= 0):
                return BAD, (
                    f"OPENROUTER_API_KEY has used its whole ${limit:.2f} limit, so the bot cannot run. "
                    "Raise the limit or add credit in OpenRouter."
                )
            return OK, f"OPENROUTER_API_KEY works: ${usage:.2f} used of its ${limit:.2f} limit."
        if status in (401, 403):
            return BAD, "OpenRouter does not accept OPENROUTER_API_KEY. Create a new key and save it again."
    return UNSURE, f"OpenRouter did not answer normally (HTTP {status})."


def check_asknews(client_id: str | None, secret: str | None, api_key: str | None, post=None) -> tuple[str, str]:
    post = post or http
    if api_key and not (client_id and secret):
        return UNSURE, "ASKNEWS_API_KEY is set. It is checked by the practice run."
    if not (client_id and secret):
        missing = [n for n, v in (("ASKNEWS_CLIENT_ID", client_id), ("ASKNEWS_SECRET", secret)) if not v]
        return BAD, f"{' and '.join(missing)} missing."
    basic = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    form = urllib.parse.urlencode({"grant_type": "client_credentials", "scope": "news"}).encode()
    status, _ = post(
        "https://auth.asknews.app/oauth2/token",
        {"Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"},
        form,
    )
    if status == 200:
        return OK, "ASKNEWS_CLIENT_ID and ASKNEWS_SECRET work."
    if status in (400, 401, 403):
        return BAD, "AskNews does not accept ASKNEWS_CLIENT_ID and ASKNEWS_SECRET. Copy them again."
    return UNSURE, f"AskNews did not answer normally (HTTP {status}). The practice run will show whether they work."


def _safely(check, *args) -> tuple[str, str]:
    """One check that crashes must not hide the others' results."""
    try:
        return check(*args)
    except Exception as e:
        return UNSURE, f"The {check.__name__} step failed ({type(e).__name__}); try again later."


def main() -> int:
    # The bot trims spaces and line breaks from these too (bot_helpers.drop_blank_env_vars).
    env = {k: (os.getenv(k) or "").strip() or None for k in (
        "METACULUS_TOKEN", "OPENROUTER_API_KEY", "ASKNEWS_CLIENT_ID", "ASKNEWS_SECRET", "ASKNEWS_API_KEY")}
    researcher = (os.getenv("RESEARCHER") or "").strip() or bot_config.DEFAULT_RESEARCHER
    results = [
        _safely(check_metaculus, env["METACULUS_TOKEN"]),
        _safely(check_forecast_data, env["METACULUS_TOKEN"]),
        _safely(check_openrouter, env["OPENROUTER_API_KEY"]),
    ]
    if researcher.startswith("asknews/"):
        results.append(_safely(check_asknews, env["ASKNEWS_CLIENT_ID"], env["ASKNEWS_SECRET"], env["ASKNEWS_API_KEY"]))
    else:
        results.append((OK, f"AskNews keys are not needed (RESEARCHER={researcher})."))
    lines = [f"- **{verdict}**: {message}" for verdict, message in results]
    print("\n".join(lines))
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Key check\n\n" + "\n".join(lines) + "\n")
    return 1 if any(verdict == BAD for verdict, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
