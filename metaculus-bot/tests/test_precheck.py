from forecasting_tools import MetaculusClient

import precheck


def test_tournaments_match_the_library():
    assert precheck.DEFAULT_TOURNAMENTS == (
        str(MetaculusClient.CURRENT_AI_COMPETITION_ID),
        str(MetaculusClient.CURRENT_MINIBENCH_ID),
    )


def test_url_asks_for_open_questions_in_one_tournament():
    url = precheck.build_url("minibench")
    assert url.startswith("https://www.metaculus.com/api/posts/?")
    assert "tournaments=minibench" in url
    assert "statuses=open" in url


def test_nothing_open_means_skip():
    def fetch(url, token):
        return {"count": 0, "results": []}

    assert precheck.has_open_questions(["33121", "minibench"], "t", fetch) is False


def test_any_open_question_means_run():
    def fetch(url, token):
        if "minibench" in url:
            return {"count": 2, "results": [{"id": 1}]}
        return {"count": 0, "results": []}

    assert precheck.has_open_questions(["33121", "minibench"], "t", fetch) is True


def test_results_without_count_are_counted():
    assert precheck.count_open({"results": [{"id": 1}]}) == 1


def test_errors_fail_open_so_no_question_is_missed():
    def fetch(url, token):
        raise OSError("network down")

    assert precheck.has_open_questions(["33121"], "t", fetch) is True


def test_unexpected_payload_fails_open():
    def fetch(url, token):
        return {"detail": "Invalid token."}

    assert precheck.has_open_questions(["33121"], "t", fetch) is True


def test_writes_github_output(tmp_path, monkeypatch):
    out = tmp_path / "out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setattr(precheck, "has_open_questions", lambda t, token: False)
    assert precheck.main([]) == 0
    assert out.read_text() == "has_open=false\n"
