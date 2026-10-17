import check_keys
from check_keys import BAD, OK, UNSURE


def _answer(status, body=None):
    return lambda url, headers, *rest: (status, body)


def test_missing_keys_are_problems():
    assert check_keys.check_metaculus(None)[0] == BAD
    assert check_keys.check_openrouter(None)[0] == BAD
    verdict, message = check_keys.check_asknews(None, "s", None)
    assert verdict == BAD and "ASKNEWS_CLIENT_ID" in message


def test_metaculus_token_accepted_for_a_bot():
    verdict, message = check_keys.check_metaculus("t", _answer(200, {"username": "my-bot", "is_bot": True}))
    assert verdict == OK and "my-bot" in message


def test_metaculus_human_token_is_flagged():
    verdict, message = check_keys.check_metaculus("t", _answer(200, {"username": "yh", "is_bot": False}))
    assert verdict == BAD and "not a bot" in message


def test_metaculus_rejected_token():
    assert check_keys.check_metaculus("t", _answer(401))[0] == BAD
    assert check_keys.check_metaculus("t", _answer(503))[0] == UNSURE


def test_openrouter_needs_a_limit():
    verdict, message = check_keys.check_openrouter("k", _answer(200, {"data": {"limit": None, "usage": 0}}))
    assert verdict == BAD and "no spending limit" in message
    verdict, message = check_keys.check_openrouter("k", _answer(200, {"data": {"limit": 40, "usage": 1.5}}))
    assert verdict == OK and "$1.50 used of its $40.00 limit" in message


def test_asknews_credentials():
    assert check_keys.check_asknews("id", "s", None, _answer(200, {}))[0] == OK
    assert check_keys.check_asknews("id", "s", None, _answer(401))[0] == BAD
    assert check_keys.check_asknews(None, None, "key")[0] == UNSURE


def test_openrouter_limit_used_up_or_resetting_is_a_problem():
    verdict, message = check_keys.check_openrouter("k", _answer(200, {"data": {"limit": 30, "usage": 30.0, "limit_remaining": 0}}))
    assert verdict == BAD and "used its whole $30.00 limit" in message
    verdict, message = check_keys.check_openrouter("k", _answer(200, {"data": {"limit": 30, "usage": 1, "limit_reset": "monthly"}}))
    assert verdict == BAD and "monthly" in message


def test_forecast_data_check_reports_counts():
    body = {"count": 1, "results": [{"id": 1, "question": {"status": "open", "my_forecasts": {"history": []}}}]}
    verdict, message = check_keys.check_forecast_data("t", _answer(200, body))
    assert verdict == OK
    assert "1 open question(s), 1 not forecast yet" in message


def test_forecast_data_missing_is_flagged():
    body = {"count": 1, "results": [{"id": 1, "question": {"status": "open", "my_forecasts": None}}]}
    verdict, message = check_keys.check_forecast_data("t", _answer(200, body))
    assert verdict == UNSURE and "did not show the bot's own forecasts" in message


def test_forecast_data_unreadable_post_is_unsure_not_a_crash():
    body = {"count": 1, "results": [{"id": 50, "group_of_questions": {}}]}
    verdict, message = check_keys.check_forecast_data("t", _answer(200, body))
    assert verdict == UNSURE and "Could not read" in message


def test_asknews_skipped_when_another_researcher_is_used(capsys, monkeypatch):
    for k in ("ASKNEWS_CLIENT_ID", "ASKNEWS_SECRET", "ASKNEWS_API_KEY", "GITHUB_STEP_SUMMARY"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("RESEARCHER", "no_research")
    monkeypatch.setattr(check_keys, "check_metaculus", lambda token: (OK, "m"))
    monkeypatch.setattr(check_keys, "check_forecast_data", lambda token: (OK, "f"))
    monkeypatch.setattr(check_keys, "check_openrouter", lambda key: (OK, "o"))
    assert check_keys.main() == 0
    assert "AskNews keys are not needed" in capsys.readouterr().out


def test_one_crashing_check_does_not_hide_the_others(capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

    def boom(token):
        raise KeyError("x")

    monkeypatch.setattr(check_keys, "check_metaculus", boom)
    monkeypatch.setattr(check_keys, "check_forecast_data", lambda token: (OK, "f"))
    monkeypatch.setattr(check_keys, "check_openrouter", lambda key: (OK, "o"))
    monkeypatch.setattr(check_keys, "check_asknews", lambda *a: (OK, "a"))
    check_keys.main()
    out = capsys.readouterr().out
    assert "boom step failed" in out and "**OK**: o" in out


def test_secrets_never_appear_in_output(capsys, monkeypatch):
    monkeypatch.setenv("METACULUS_TOKEN", "secret-token-123")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-secret-456")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr(check_keys, "http", lambda *a, **k: (401, None))
    assert check_keys.main() == 1
    out = capsys.readouterr().out
    assert "secret-token-123" not in out and "sk-or-secret-456" not in out
