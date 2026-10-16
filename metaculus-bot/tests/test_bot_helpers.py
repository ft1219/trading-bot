import os

from bot_helpers import drop_blank_env_vars


def test_blank_keys_are_removed_and_real_ones_kept(monkeypatch):
    monkeypatch.setenv("ASKNEWS_API_KEY", "")
    monkeypatch.setenv("ASKNEWS_SECRET", "   ")
    monkeypatch.setenv("ASKNEWS_CLIENT_ID", "real-id")
    removed = drop_blank_env_vars()
    assert sorted(removed) == ["ASKNEWS_API_KEY", "ASKNEWS_SECRET"]
    assert "ASKNEWS_API_KEY" not in os.environ
    assert os.environ["ASKNEWS_CLIENT_ID"] == "real-id"
