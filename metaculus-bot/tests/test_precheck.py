from forecasting_tools import MetaculusClient

import precheck


def _question(forecast: bool, status: str = "open") -> dict:
    history = [{"start_time": 1}] if forecast else []
    return {"id": 1, "status": status, "my_forecasts": {"history": history, "latest": None}}


def _payload(*posts) -> dict:
    return {"count": len(posts), "results": list(posts)}


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
    assert "limit=100" in url


def test_nothing_open_means_skip():
    def fetch(url, token):
        return _payload()

    assert precheck.has_questions_to_forecast(["33121", "minibench"], "t", fetch) is False


def test_open_but_already_forecast_means_skip():
    def fetch(url, token):
        return _payload({"id": 10, "question": _question(forecast=True)})

    assert precheck.has_questions_to_forecast(["33121", "minibench"], "t", fetch) is False


def test_a_new_question_means_run():
    def fetch(url, token):
        if "minibench" in url:
            return _payload(
                {"id": 10, "question": _question(forecast=True)},
                {"id": 11, "question": _question(forecast=False)},
            )
        return _payload()

    assert precheck.has_questions_to_forecast(["33121", "minibench"], "t", fetch) is True


def test_group_subquestions_are_checked_one_by_one():
    done = {"id": 10, "group_of_questions": {"questions": [_question(True), _question(True)]}}
    one_new = {"id": 11, "group_of_questions": {"questions": [_question(True), _question(False)]}}
    closed_new = {"id": 12, "group_of_questions": {"questions": [_question(False, status="closed")]}}
    assert precheck.count_to_forecast(_payload(done, closed_new)) == 0
    assert precheck.count_to_forecast(_payload(done, one_new)) == 1


def test_conditional_reads_forecasts_like_the_library():
    def conditional(yes, no):
        return {"id": 20, "conditional": {"question_yes": yes, "question_no": no}}

    assert precheck.count_to_forecast(_payload(conditional(_question(True), _question(False)))) == 0
    assert precheck.count_to_forecast(_payload(conditional(_question(False), _question(True)))) == 1
    no_data = {"id": 2, "status": "open"}
    assert precheck.count_to_forecast(_payload(conditional(no_data, _question(True)))) == 0


def test_missing_forecast_data_counts_as_new():
    # Without a valid token Metaculus leaves out my_forecasts.
    post = {"id": 30, "question": {"id": 3, "status": "open"}}
    assert precheck.count_to_forecast(_payload(post)) == 1


def test_notebooks_are_ignored():
    assert precheck.count_to_forecast(_payload({"id": 40, "notebook": {}})) == 0


def test_more_posts_than_one_page_means_run():
    payload = {"count": 150, "results": [{"id": 1, "question": _question(True)}]}
    assert precheck.count_to_forecast(payload) > 0


def test_errors_fail_open_so_no_question_is_missed():
    def fetch(url, token):
        raise OSError("network down")

    assert precheck.has_questions_to_forecast(["33121"], "t", fetch) is True


def test_unexpected_payload_fails_open():
    def fetch(url, token):
        return {"detail": "Invalid token."}

    assert precheck.has_questions_to_forecast(["33121"], "t", fetch) is True


def test_unexpected_post_shape_fails_open():
    def fetch(url, token):
        return _payload({"id": 50, "group_of_questions": {}})

    assert precheck.has_questions_to_forecast(["33121"], "t", fetch) is True


def test_writes_github_output(tmp_path, monkeypatch):
    out = tmp_path / "out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setattr(precheck, "has_questions_to_forecast", lambda t, token: False)
    assert precheck.main([]) == 0
    assert out.read_text() == "to_forecast=false\n"
