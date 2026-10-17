import json

import pytest

import timer_setup

GH_TOKEN = "github_pat_secret123"
CRON_KEY = "cron-secret456"


class FakeApis:
    """Stands in for the GitHub and cron-job.org APIs."""

    def __init__(self, github_get=200, dispatch=204, cron_list=200):
        self.github_get = github_get
        self.dispatch = dispatch
        self.cron_list = cron_list
        self.jobs = {}
        self.calls = []

    def __call__(self, method, url, token, body=None, extra=None):
        self.calls.append((method, url, token))
        if "api.github.com" in url:
            if method == "GET":
                return self.github_get, {"name": "Bots - every 40 minutes", "state": "active"}
            return self.dispatch, None
        if url.endswith("/jobs") and method == "GET":
            jobs = [{"jobId": k, "title": v["title"]} for k, v in self.jobs.items()]
            return self.cron_list, {"jobs": jobs, "someFailed": False}
        if url.endswith("/jobs") and method == "PUT":
            job_id = 100 + len(self.jobs)
            self.jobs[job_id] = body["job"]
            return 200, {"jobId": job_id}
        if url.endswith("/history"):
            return 200, {"history": [], "predictions": [1792220820]}
        job_id = int(url.rsplit("/", 1)[1])
        if method == "PATCH":
            self.jobs[job_id] = body["job"]
            return 200, {}
        return 200, {"jobDetails": self.jobs[job_id]}


@pytest.fixture
def apis(monkeypatch):
    fake = FakeApis()
    monkeypatch.setattr(timer_setup, "call", fake)
    monkeypatch.setattr(timer_setup.time, "sleep", lambda s: None)
    monkeypatch.setenv("BOT_TIMER_TOKEN", GH_TOKEN)
    monkeypatch.setenv("CRONJOB_API_KEY", CRON_KEY)
    return fake


def test_jobs_start_the_workflow_every_40_minutes():
    starts = sorted(h * 60 + m for _, hours, minutes in timer_setup.JOBS for h in hours for m in minutes)
    assert len(starts) == 36
    gaps = {b - a for a, b in zip(starts, starts[1:])} | {starts[0] + 24 * 60 - starts[-1]}
    assert gaps == {40}


def test_creates_both_jobs_that_post_to_the_dispatch_endpoint(apis):
    assert timer_setup.main() == 0
    assert len(apis.jobs) == 2
    for job in apis.jobs.values():
        assert job["enabled"] is True
        assert job["requestMethod"] == 1
        assert job["url"].endswith("/actions/workflows/metaculus-forecast.yaml/dispatches")
        assert job["extendedData"]["headers"]["Authorization"] == f"Bearer {GH_TOKEN}"
        assert json.loads(job["extendedData"]["body"]) == {"ref": "main"}
        assert job["schedule"]["timezone"] == "UTC"


def test_running_again_updates_instead_of_duplicating(apis):
    assert timer_setup.main() == 0
    assert timer_setup.main() == 0
    assert len(apis.jobs) == 2
    assert sum(1 for method, _, _ in apis.calls if method == "PATCH") == 2


def test_never_prints_either_secret(apis, capsys):
    assert timer_setup.main() == 0
    out = capsys.readouterr().out
    assert GH_TOKEN not in out
    assert CRON_KEY not in out


def test_missing_secret_stops_before_any_call(apis, monkeypatch, capsys):
    monkeypatch.setenv("CRONJOB_API_KEY", "  ")
    assert timer_setup.main() == 1
    assert apis.calls == []
    assert "CRONJOB_API_KEY" in capsys.readouterr().out


@pytest.mark.parametrize("field", ["github_get", "dispatch", "cron_list"])
def test_a_refused_key_stops_without_creating_jobs(apis, field):
    setattr(apis, field, 403)
    assert timer_setup.main() == 1
    assert apis.jobs == {}
