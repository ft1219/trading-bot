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
