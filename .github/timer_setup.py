"""
One-off: create (or update) the two cron-job.org jobs that start the
"Metaculus - forecast new questions" workflow every 40 minutes, because
GitHub's own schedule has not fired for this repo.

Needs secrets BOT_TIMER_TOKEN (fine-grained GitHub token, this repo only,
Actions: read and write) and CRONJOB_API_KEY (cron-job.org API key).
Never prints either secret.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

REPO = "ft1219/trading-bot"
WORKFLOW = "metaculus-forecast.yaml"
DISPATCH_URL = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches"
CRON_API = "https://api.cron-job.org"

# :07 and :47 of even hours, :27 of odd hours (UTC): one run every 40 minutes.
JOBS = [
    ("Metaculus bot timer - even hours", list(range(0, 24, 2)), [7, 47]),
    ("Metaculus bot timer - odd hours", list(range(1, 24, 2)), [27]),
]


def call(method: str, url: str, token: str, body: dict | None = None, extra: dict | None = None):
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "trading-bot-timer-setup"}
    headers.update(extra or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()[:500].decode(errors="replace")
        return e.code, raw


def main() -> int:
    gh_token = os.environ.get("BOT_TIMER_TOKEN", "").strip()
    cron_key = os.environ.get("CRONJOB_API_KEY", "").strip()
    missing = [n for n, v in (("BOT_TIMER_TOKEN", gh_token), ("CRONJOB_API_KEY", cron_key)) if not v]
    if missing:
        print(f"::error::Missing secret(s): {', '.join(missing)}")
        return 1

    gh_extra = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

    # 1. The GitHub key can see the workflow and start it.
    status, body = call("GET", f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}", gh_token, extra=gh_extra)
    if status != 200:
        print(f"::error::BOT_TIMER_TOKEN cannot read the workflow (HTTP {status}). "
              "Check it was made for trading-bot with Actions: Read and write.")
        return 1
    print(f"GitHub key can see workflow '{body.get('name')}' (state {body.get('state')}).")
    status, body = call("POST", DISPATCH_URL, gh_token, body={"ref": "main"}, extra=gh_extra)
    if status not in (200, 204):
        print(f"::error::BOT_TIMER_TOKEN cannot start the workflow (HTTP {status}): {body}")
        return 1
    print(f"GitHub key started one forecasting run (HTTP {status}).")

    # 2. cron-job.org: update our jobs if they exist, otherwise create them.
    status, body = call("GET", f"{CRON_API}/jobs", cron_key)
    if status != 200:
        print(f"::error::CRONJOB_API_KEY was refused by cron-job.org (HTTP {status}): {body}")
        return 1
    existing = {j.get("title"): j.get("jobId") for j in (body or {}).get("jobs", [])}
    print(f"cron-job.org account has {len(existing)} job(s) before setup.")

    ids = []
    for title, hours, minutes in JOBS:
        job = {
            "url": DISPATCH_URL,
            "enabled": True,
            "title": title,
            "saveResponses": False,
            "requestTimeout": 30,
            "requestMethod": 1,  # POST
            "schedule": {
                "timezone": "UTC",
                "expiresAt": 0,
                "hours": hours,
                "mdays": [-1],
                "minutes": minutes,
                "months": [-1],
                "wdays": [-1],
            },
            "extendedData": {
                "headers": {
                    "Authorization": f"Bearer {gh_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                    "Content-Type": "application/json",
                },
                "body": json.dumps({"ref": "main"}),
            },
        }
        if title in existing:
            job_id = existing[title]
            status, body = call("PATCH", f"{CRON_API}/jobs/{job_id}", cron_key, body={"job": job})
            action = "updated"
        else:
            status, body = call("PUT", f"{CRON_API}/jobs", cron_key, body={"job": job})
            job_id = (body or {}).get("jobId") if isinstance(body, dict) else None
            action = "created"
        if status != 200 or job_id is None:
            print(f"::error::Could not set up '{title}' (HTTP {status}): {body}")
            return 1
        print(f"{action} '{title}' as job {job_id}.")
        ids.append(job_id)
        time.sleep(13)  # create is limited to 5 a minute

    # 3. Read back what cron-job.org stored and when it will next run.
    for job_id in ids:
        status, body = call("GET", f"{CRON_API}/jobs/{job_id}", cron_key)
        if status != 200:
            print(f"::error::Could not read back job {job_id} (HTTP {status}): {body}")
            return 1
        d = body["jobDetails"]
        sch = d["schedule"]
        hdrs = sorted((d.get("extendedData") or {}).get("headers", {}).keys())
        print(f"job {job_id}: enabled={d['enabled']} method={d['requestMethod']} "
              f"hours={sch['hours']} minutes={sch['minutes']} tz={sch['timezone']} "
              f"header names={hdrs} body={(d.get('extendedData') or {}).get('body')!r}")
        status, hist = call("GET", f"{CRON_API}/jobs/{job_id}/history", cron_key)
        if status == 200:
            nxt = [time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(t)) for t in hist.get("predictions", [])]
            print(f"job {job_id}: next runs {nxt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
