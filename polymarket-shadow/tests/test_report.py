import datetime as dt
import json

import report
from selection import Settings


def write_day(root, day, ts, rewards_low, value, rebates=0.0, pilot=True, samples=36):
    folder = root / "days" / day
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "samples.jsonl", "w") as f:
        for i in range(samples):
            per = {"est_low": rewards_low / samples, "est_high": 2 * rewards_low / samples,
                   "value": value, "rebates": rebates, "fills": 0, "yes": 0, "no": 0, "q": 1,
                   "share_low": 0.1, "share_high": 0.2, "bid": 0.5, "ask": 0.6}
            f.write(json.dumps({"ts": ts + i * 2400, "condition_id": "0xm", "pilot": pilot, "dt": 2400,
                                "levels": {"1": per}}) + "\n")


def days(n):
    return [f"2026-10-{d:02d}" for d in range(1, n + 1)]


def test_not_enough_days(tmp_path):
    for i, d in enumerate(days(5)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=5, value=0)
    text, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    assert summary["gate_a"]["verdict"] == "NOT ENOUGH DATA YET"


def test_pass_and_fail(tmp_path):
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=2.0, value=0)
    _, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    assert summary["gate_a"]["verdict"] == "PASS"
    assert abs(summary["gate_a"]["mean_cautious_usd_per_day"] - 2.0) < 1e-9


def test_trading_losses_count_and_small_rewards_pay_nothing(tmp_path):
    # 0.90/day of rewards is under the $1 payout minimum, and the position loses 0.10/day.
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=0.9, value=-0.1 * (i + 1))
    _, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    assert summary["gate_a"]["verdict"] == "FAIL"
    assert round(summary["gate_a"]["mean_cautious_usd_per_day"], 6) == -0.1
    day = summary["days"][3]["levels"]["1"]
    assert round(day["pilot_optimistic"], 6) == round(1.8 - 0.1, 6)  # 1.80 high estimate clears $1 together


def test_partial_days_do_not_count(tmp_path):
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=5, value=0, samples=10)
    _, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    assert summary["gate_a"]["days"] == 0


def test_thin_markets_are_listed_apart_and_never_count(tmp_path):
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=2.0, value=0)
        with open(tmp_path / "days" / d / "samples.jsonl", "a") as f:
            for j in range(36):
                per = {"est_low": 0.0, "est_high": 50 / 36, "value": 0.0, "rebates": 0.0, "fills": 0}
                f.write(json.dumps({"ts": 1790000000 + i * 86400 + j * 2400, "condition_id": "0xthin",
                                    "pilot": False, "thin": True, "dt": 2400, "levels": {"1": per}}) + "\n")
    text, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    lv = summary["days"][-1]["levels"]["1"]
    assert lv["thin_markets"] == 1 and lv["all_markets"] == 1
    assert abs(lv["thin_rewards_high"] - 50) < 1e-9 and abs(lv["all_rewards_high"] - 4.0) < 1e-9
    assert abs(summary["gate_a"]["mean_cautious_usd_per_day"] - 2.0) < 1e-9
    assert "Thin markets (1 watched)" in text


def test_running_totals_older_than_the_report_window_are_not_counted_again(tmp_path):
    # 40 days of a pilot whose rebates grow $0.50 a day: no day may show the whole running total.
    for i in range(40):
        d = (dt.date(2026, 9, 1) + dt.timedelta(days=i)).isoformat()
        write_day(tmp_path, d, 1788220800 + i * 86400, rewards_low=1.4, value=0, rebates=0.5 * (i + 1))
    rows = report.daily_rows(tmp_path, 1, 1788220800 + 50 * 86400)
    assert len(rows) == 40
    assert all(abs(r["levels"]["1"]["pilot_cautious"] - 1.4) < 1e-9 for r in rows)  # rebates stay under $1
    _, summary = report.build(tmp_path, Settings(), now=1788220800 + 50 * 86400)
    assert len(summary["days"]) == report.REPORT_DAYS


def test_a_market_counts_as_pilot_only_while_it_is_one(tmp_path):
    d = "2026-10-05"
    folder = tmp_path / "days" / d
    folder.mkdir(parents=True)
    base = 1791158400  # 2026-10-05 00:00 UTC
    per = lambda low: {"est_low": low, "est_high": low, "value": 0.0, "rebates": 0.0}
    rows = [{"ts": base + 420, "condition_id": "0xold", "pilot": True, "dt": 2400, "levels": {"1": per(0.5)}}]
    for i in range(1, 36):  # yesterday's pilot, demoted at 00:47, and the new pilot
        rows.append({"ts": base + 420 + i * 2400, "condition_id": "0xold", "pilot": False, "dt": 2400,
                     "levels": {"1": per(0.5)}})
        rows.append({"ts": base + 420 + i * 2400, "condition_id": "0xnew", "pilot": True, "dt": 2400,
                     "levels": {"1": per(0.1)}})
    (folder / "samples.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (folder / "watchlist.jsonl").write_text(
        json.dumps({"ts": base + 2820, "condition_id": "0xnew", "pilot": True}) + "\n"
        + json.dumps({"ts": base + 2820, "condition_id": "0xold", "pilot": False}) + "\n")
    lv = report.daily_rows(tmp_path, 1, base + 86400)[0]["levels"]["1"]
    assert abs(lv["pilot_rewards_low"] - (0.5 + 3.5)) < 1e-9  # each pilot only for the time it was one
    assert lv["pilot_covered"]  # judged on the day's final pilot set


def test_a_closeout_after_a_sample_is_measured_from_that_sample(tmp_path):
    folder = tmp_path / "days" / "2026-10-05"
    folder.mkdir(parents=True)
    base = 1791158400
    sample = {"ts": base + 420, "condition_id": "0xm", "pilot": False, "dt": 2400,
              "levels": {"1": {"est_low": 0, "est_high": 0, "value": 3.0, "rebates": 0.4}}}
    closeout = {"ts": base + 2820, "condition_id": "0xm", "level": 1, "pilot": False, "value_after": 2.5,
                "rebates": 0.4}
    (folder / "samples.jsonl").write_text(json.dumps(sample) + "\n")
    (folder / "closeouts.jsonl").write_text(json.dumps(closeout) + "\n")
    lv = report.daily_rows(tmp_path, 1, base + 86400)[0]["levels"]["1"]
    assert abs(lv["all_trading"] - 2.5) < 1e-9 and abs(lv["all_rebates"] - 0.4) < 1e-9


def test_today_is_labelled_as_unfinished(tmp_path):
    write_day(tmp_path, "2026-10-01", 1790812800, rewards_low=5, value=0)
    text, _ = report.build(tmp_path, Settings(), now=1790812800 + 3600)
    assert "2026-10-01 (today, so far)" in text


def test_trading_losses_on_badly_covered_days_still_count(tmp_path):
    names = days(16)
    for i, d in enumerate(names):
        if i == 4:  # a partial day that loses $20: it is not a well-covered day, but the loss counts
            write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=9, value=-20, samples=10)
        else:
            write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=2.0, value=0 if i < 4 else -20)
    _, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    gate = summary["gate_a"]
    assert gate["decided_on"] == names[14] and gate["days"] == 15 and gate["days_since_start"] == 16
    assert abs(gate["mean_cautious_usd_per_day"] - (2.0 - 20 / 15)) < 1e-9 and gate["verdict"] == "FAIL"
    assert abs(gate["running_cautious_usd_per_day"] - (2.0 - 20 / 16)) < 1e-9


def test_the_verdict_is_taken_once_and_later_days_do_not_change_it(tmp_path):
    # 14 good days, then 26 days losing $3 a day: the verdict stays PASS, the running average shows the slide.
    for i in range(40):
        d = (dt.date(2026, 9, 1) + dt.timedelta(days=i)).isoformat()
        write_day(tmp_path, d, 1788220800 + i * 86400, rewards_low=2.0, value=-3.0 * max(0, i - 13))
    text, summary = report.build(tmp_path, Settings(), now=1788220800 + 50 * 86400)
    gate = summary["gate_a"]
    assert gate["verdict"] == "PASS" and gate["decided_on"] == "2026-09-14"
    assert abs(gate["mean_cautious_usd_per_day"] - 2.0) < 1e-9
    assert abs(gate["running_cautious_usd_per_day"] - (2.0 - 78 / 40)) < 1e-9 and gate["days"] == 40
    assert "Decided on 2026-09-14" in text


def test_no_verdict_when_the_pilot_settings_differ_from_the_plan(tmp_path):
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=2.0, value=0)
    _, summary = report.build(tmp_path, Settings(budget_per_market_usd=50), now=1790000000 + 30 * 86400)
    assert summary["gate_a"]["verdict"].startswith("NO VERDICT")


def test_a_sample_without_a_book_counts_no_reward_and_leaves_the_value_alone(tmp_path):
    folder = tmp_path / "days" / "2026-10-05"
    folder.mkdir(parents=True)
    base = 1791158400
    row = lambda ts, low, value: {"ts": ts, "condition_id": "0xm", "pilot": True, "dt": 2400,
                                  "levels": {"1": {"est_low": low, "est_high": low, "value": value, "rebates": 0}}}
    rows = [row(base + 2400, 0.1, -1.0), row(base + 4800, 0.0, None), row(base + 7200, 0.1, -1.5)]
    (folder / "samples.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    lv = report.daily_rows(tmp_path, 1, base + 86400)[0]["levels"]["1"]
    assert abs(lv["pilot_rewards_low"] - 0.2) < 1e-9 and abs(lv["pilot_trading"] + 1.5) < 1e-9


def test_a_thin_market_closed_out_after_leaving_the_list_stays_thin(tmp_path):
    folder = tmp_path / "days" / "2026-10-05"
    folder.mkdir(parents=True)
    closeout = {"ts": 1791158820, "condition_id": "0xthin", "level": 1, "pilot": False, "thin": True,
                "value_after": -2.0, "rebates": 0}
    (folder / "closeouts.jsonl").write_text(json.dumps(closeout) + "\n")
    lv = report.daily_rows(tmp_path, 1, 1791158400 + 86400)[0]["levels"]["1"]
    assert lv["thin_markets"] == 1 and lv["all_markets"] == 0 and abs(lv["thin_trading"] + 2.0) < 1e-9


def test_the_trades_only_comparison_is_reported_but_not_judged(tmp_path):
    for i, d in enumerate(days(15)):
        write_day(tmp_path, d, 1790000000 + i * 86400, rewards_low=2.0, value=-1.0 * (i + 1))
        path = tmp_path / "days" / d / "samples.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        for r in rows:
            r["levels"]["1"]["value_trades_only"] = -0.2 * (i + 1)
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    text, summary = report.build(tmp_path, Settings(), now=1790000000 + 30 * 86400)
    gate = summary["gate_a"]
    assert abs(gate["mean_cautious_usd_per_day"] - 1.0) < 1e-9 and gate["verdict"] == "FAIL"
    assert abs(gate["mean_trades_only_usd_per_day"] - 1.8) < 1e-9
    assert abs(summary["days"][3]["levels"]["1"]["pilot_trading_trades_only"] + 0.2) < 1e-9
    assert "If only trades could fill paper orders" in text and "-$0.20" in text


def test_the_report_says_when_it_was_updated_and_how_runs_went(tmp_path):
    write_day(tmp_path, "2026-10-01", 1790812800, rewards_low=5, value=0)
    (tmp_path / "days" / "2026-10-01" / "runs.jsonl").write_text(
        json.dumps({"ts": 1790812800 + 600, "errors": []}) + "\n"
        + json.dumps({"ts": 1790812800 + 3000, "errors": ["0xabc: no book"]}) + "\n")
    text, _ = report.build(tmp_path, Settings(), now=1790812800 + 3600, this_run={"errors": ["books: boom"]})
    assert "Last updated 2026-10-01 01:00 UTC; 3 run(s) in the last 24 hours, 2 with problems noted" in text
