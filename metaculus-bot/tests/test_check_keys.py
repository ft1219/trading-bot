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


def test_forecast_data_check_reports_counts():
    body = {"count": 1, "results": [{"id": 1, "question": {"status": "open", "my_forecasts": {"history": []}}}]}
    verdict, message = check_keys.check_forecast_data("t", _answer(200, body))
    assert verdict == OK
    assert "1 not forecast yet, 1 with forecast data" in message


def test_secrets_never_appear_in_output(capsys, monkeypatch):
    monkeypatch.setenv("METACULUS_TOKEN", "secret-token-123")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-secret-456")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr(check_keys, "http", lambda *a, **k: (401, None))
    assert check_keys.main() == 1
    out = capsys.readouterr().out
    assert "secret-token-123" not in out and "sk-or-secret-456" not in out
