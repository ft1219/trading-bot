from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from bot_config import (
    DEFAULT_FORECAST_MODEL,
    DEFAULT_TOURNAMENT_FORECAST_MODEL,
    DEFAULT_MAX_COST_PER_RUN_USD,
    DEFAULT_MAX_QUESTIONS_PER_RUN,
    OPENAI_FORECAST_MODEL,
    SettingsError,
    forecaster_kwargs,
    load_settings,
    pick_questions_to_forecast,
    reasoning_kwargs,
)


def test_defaults_when_nothing_is_set():
    settings = load_settings({})
    assert settings.forecast_model == DEFAULT_FORECAST_MODEL
    assert settings.tournament_forecast_model == DEFAULT_TOURNAMENT_FORECAST_MODEL
    assert settings.max_questions_per_run == DEFAULT_MAX_QUESTIONS_PER_RUN
    assert settings.max_cost_per_run_usd == DEFAULT_MAX_COST_PER_RUN_USD
    assert settings.forecast_reasoning is True


def test_blank_values_fall_back_to_defaults():
    # GitHub passes unset repository variables as empty strings.
    settings = load_settings(
        {"FORECAST_MODEL": "", "TOURNAMENT_FORECAST_MODEL": "", "MAX_COST_PER_RUN_USD": "  "}
    )
    assert settings.forecast_model == DEFAULT_FORECAST_MODEL
    assert settings.tournament_forecast_model == DEFAULT_TOURNAMENT_FORECAST_MODEL
    assert settings.max_cost_per_run_usd == DEFAULT_MAX_COST_PER_RUN_USD


def test_overrides_are_read():
    settings = load_settings(
        {
            "FORECAST_MODEL": "openrouter/deepseek/deepseek-v4-pro",
            "TOURNAMENT_FORECAST_MODEL": "openrouter/anthropic/claude-sonnet-5.5",
            "FORECAST_REASONING": "false",
            "PREDICTIONS_PER_QUESTION": "3",
            "MAX_QUESTIONS_PER_RUN": "4",
            "MAX_COST_PER_RUN_USD": "0.25",
        }
    )
    assert settings.forecast_model == "openrouter/deepseek/deepseek-v4-pro"
    assert settings.tournament_forecast_model == "openrouter/anthropic/claude-sonnet-5.5"
    assert settings.forecast_reasoning is False
    assert settings.predictions_per_question == 3
    assert settings.max_questions_per_run == 4
    assert settings.max_cost_per_run_usd == 0.25


@pytest.mark.parametrize("value", ["0", "-1", "abc"])
def test_cost_limit_cannot_be_removed_or_garbled(value):
    # 0 would mean "unlimited" to the cost manager, so it must be refused.
    with pytest.raises(SettingsError):
        load_settings({"MAX_COST_PER_RUN_USD": value})


@pytest.mark.parametrize("value", ["0", "two"])
def test_question_cap_must_be_a_positive_whole_number(value):
    with pytest.raises(SettingsError):
        load_settings({"MAX_QUESTIONS_PER_RUN": value})


def test_bad_boolean_is_refused():
    with pytest.raises(SettingsError):
        load_settings({"FORECAST_REASONING": "maybe"})


def test_reasoning_is_requested_only_for_openrouter_models():
    on = load_settings({})
    assert reasoning_kwargs(on) == {"extra_body": {"reasoning": {"enabled": True}}}
    off = load_settings({"FORECAST_REASONING": "no"})
    assert reasoning_kwargs(off) == {}
    other = load_settings({"FORECAST_MODEL": "gpt-4o"})
    assert reasoning_kwargs(other) == {}
    assert reasoning_kwargs(on, "gpt-4o") == {}
    assert reasoning_kwargs(other, DEFAULT_TOURNAMENT_FORECAST_MODEL) == {
        "extra_body": {"reasoning": {"enabled": True}}
    }


def test_openai_key_switches_minibench_to_gpt6_sol():
    assert load_settings({"OPENAI_API_KEY": "sk-test"}).forecast_model == OPENAI_FORECAST_MODEL
    assert load_settings({"OPENAI_API_KEY": "  "}).forecast_model == DEFAULT_FORECAST_MODEL
    # An explicit FORECAST_MODEL still wins over the key.
    chosen = load_settings({"OPENAI_API_KEY": "sk-test", "FORECAST_MODEL": "openrouter/x/y"})
    assert chosen.forecast_model == "openrouter/x/y"
    # The main tournament stays on Claude either way.
    assert (
        load_settings({"OPENAI_API_KEY": "sk-test"}).tournament_forecast_model
        == DEFAULT_TOURNAMENT_FORECAST_MODEL
    )


def test_claude_gets_adaptive_thinking_and_no_temperature():
    settings = load_settings({})
    assert forecaster_kwargs(settings, DEFAULT_TOURNAMENT_FORECAST_MODEL) == {
        "temperature": None,
        "max_tokens": 16000,
        "extra_body": {"reasoning": {"effort": "high"}},
    }
    # Turning reasoning off does not matter: Claude refuses a thinking budget
    # and thinks adaptively anyway.
    off = load_settings({"FORECAST_REASONING": "false"})
    assert forecaster_kwargs(off, "anthropic/claude-sonnet-5.5")["temperature"] is None


def test_openai_models_get_reasoning_effort_in_the_body():
    settings = load_settings({})
    assert forecaster_kwargs(settings, OPENAI_FORECAST_MODEL) == {
        "temperature": None,
        "extra_body": {"reasoning_effort": "high"},
    }
    off = load_settings({"FORECAST_REASONING": "false"})
    assert forecaster_kwargs(off, OPENAI_FORECAST_MODEL) == {"temperature": None}


def test_other_models_keep_temperature_and_openrouter_reasoning():
    settings = load_settings({})
    assert forecaster_kwargs(settings) == {
        "temperature": 0.3,
        "extra_body": {"reasoning": {"enabled": True}},
    }


def _question(name, closes_in_hours, forecasted=False):
    close_time = (
        None
        if closes_in_hours is None
        else datetime(2026, 10, 16, tzinfo=timezone.utc)
        + timedelta(hours=closes_in_hours)
    )
    return SimpleNamespace(
        name=name, close_time=close_time, already_forecasted=forecasted
    )


def test_picks_unforecast_questions_soonest_closing_first():
    questions = [
        _question("late", 5),
        _question("done", 1, forecasted=True),
        _question("no-close-time", None),
        _question("soon", 1),
        _question("mid", 3),
    ]
    chosen, deferred = pick_questions_to_forecast(questions, max_questions=2)
    assert [q.name for q in chosen] == ["soon", "mid"]
    assert [q.name for q in deferred] == ["late", "no-close-time"]


def test_already_forecasted_none_counts_as_not_forecasted():
    questions = [_question("unknown", 2)]
    questions[0].already_forecasted = None
    chosen, deferred = pick_questions_to_forecast(questions, max_questions=5)
    assert [q.name for q in chosen] == ["unknown"]
    assert deferred == []
