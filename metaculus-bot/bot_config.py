"""
Our settings for the Metaculus bot: which AI models it uses and how much it
may spend in one run.

Every value can be overridden with an environment variable. In GitHub
Actions these come from repository *variables* (Settings -> Secrets and
variables -> Actions -> Variables), so switching models needs no code change.

Defaults are chosen for a small budget. DeepSeek V3.2 with reasoning plus
AskNews research is the setup Metaculus ran as `metac-deepseek-3-2-reasoning
+asknews`, which placed 5th of the Metaculus baseline bots in Spring 2026 at
roughly a cent per question. The main tournament, where most of the prize
money is, gets a stronger model; MiniBench and the Cup keep DeepSeek.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

DEFAULT_FORECAST_MODEL = "openrouter/deepseek/deepseek-v3.2"
# Main tournament only. On Metaculus's FutureEval model leaderboard (October
# 2026) Gemini 3.7 Flash scores about 11.8 against 6.9 for DeepSeek 3.2 High,
# at roughly $0.08-0.20 a question. Prizes go by the square of the season
# score, so the main tournament is where a better model pays; MiniBench pays
# only its top few bots each round.
DEFAULT_TOURNAMENT_FORECAST_MODEL = "openrouter/google/gemini-3.7-flash"
DEFAULT_PARSER_MODEL = "openrouter/deepseek/deepseek-v3.2"
DEFAULT_RESEARCHER = "asknews/news-summaries"

# Template default is 5 forecasts per question, averaged. Kept as-is.
DEFAULT_PREDICTIONS_PER_QUESTION = 5
# Metaculus releases at most 5 questions at a time; 12 leaves headroom for a
# missed run while still bounding the cost of any single run.
DEFAULT_MAX_QUESTIONS_PER_RUN = 12
# A full run of 12 main-tournament questions on Gemini 3.7 Flash costs about
# $1-2.50. The season-wide cap is the spending limit set on the OpenRouter key
# itself.
DEFAULT_MAX_COST_PER_RUN_USD = 3.00
# Backstop for models litellm cannot price. A normal question takes about
# 10-15 calls (5 forecasts and their parsing); conditional questions take
# about 4 times that.
DEFAULT_MAX_LLM_CALLS_PER_RUN = 400
# Questions forecast at the same time. The spending limit is checked before
# each AI call, so the most a run can overshoot it is the calls already in
# flight: about this many questions' worth. 5 fits a whole MiniBench release
# in one batch, so a run with slow hosts (two 300 s tries per forecast) still
# ends well inside the job's time limit.
DEFAULT_QUESTIONS_IN_PARALLEL = 5


class SettingsError(ValueError):
    pass


@dataclass(frozen=True)
class BotSettings:
    forecast_model: str
    tournament_forecast_model: str
    parser_model: str
    researcher: str
    forecast_reasoning: bool
    predictions_per_question: int
    max_questions_per_run: int
    max_cost_per_run_usd: float
    max_llm_calls_per_run: int
    questions_in_parallel: int


def _text(env: Mapping[str, str], name: str, default: str) -> str:
    value = (env.get(name) or "").strip()
    return value or default


def _int(env: Mapping[str, str], name: str, default: int, minimum: int) -> int:
    raw = (env.get(name) or "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as e:
        raise SettingsError(f"{name} must be a whole number, got {raw!r}") from e
    if value < minimum:
        raise SettingsError(f"{name} must be at least {minimum}, got {value}")
    return value


def _float(env: Mapping[str, str], name: str, default: float) -> float:
    raw = (env.get(name) or "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as e:
        raise SettingsError(f"{name} must be a number, got {raw!r}") from e
    # A limit of zero or less would stop every call; refuse it as a typo.
    if value <= 0:
        raise SettingsError(f"{name} must be greater than 0, got {value}")
    return value


def _bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    raw = (env.get(name) or "").strip().lower()
    if not raw:
        return default
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off"):
        return False
    raise SettingsError(f"{name} must be true or false, got {raw!r}")


def load_settings(env: Mapping[str, str] | None = None) -> BotSettings:
    env = os.environ if env is None else env
    return BotSettings(
        forecast_model=_text(env, "FORECAST_MODEL", DEFAULT_FORECAST_MODEL),
        tournament_forecast_model=_text(
            env, "TOURNAMENT_FORECAST_MODEL", DEFAULT_TOURNAMENT_FORECAST_MODEL
        ),
        parser_model=_text(env, "PARSER_MODEL", DEFAULT_PARSER_MODEL),
        researcher=_text(env, "RESEARCHER", DEFAULT_RESEARCHER),
        forecast_reasoning=_bool(env, "FORECAST_REASONING", True),
        predictions_per_question=_int(
            env, "PREDICTIONS_PER_QUESTION", DEFAULT_PREDICTIONS_PER_QUESTION, 1
        ),
        max_questions_per_run=_int(
            env, "MAX_QUESTIONS_PER_RUN", DEFAULT_MAX_QUESTIONS_PER_RUN, 1
        ),
        max_cost_per_run_usd=_float(
            env, "MAX_COST_PER_RUN_USD", DEFAULT_MAX_COST_PER_RUN_USD
        ),
        max_llm_calls_per_run=_int(
            env, "MAX_LLM_CALLS_PER_RUN", DEFAULT_MAX_LLM_CALLS_PER_RUN, 1
        ),
        questions_in_parallel=_int(
            env, "QUESTIONS_IN_PARALLEL", DEFAULT_QUESTIONS_IN_PARALLEL, 1
        ),
    )


def reasoning_kwargs(settings: BotSettings, model: str | None = None) -> dict:
    """
    Extra request options that switch on the model's step-by-step reasoning.
    OpenRouter takes this as `reasoning: {enabled: true}` in the request body.
    """
    model = model or settings.forecast_model
    if settings.forecast_reasoning and model.startswith("openrouter/"):
        return {"extra_body": {"reasoning": {"enabled": True}}}
    return {}


def pick_questions_to_forecast(questions: list, max_questions: int) -> tuple[list, list]:
    """
    Keep questions we have not forecast yet, soonest-closing first, up to
    `max_questions`. Returns (chosen, deferred) so the caller can log what
    was left for the next run instead of dropping it silently.
    """
    fresh = [q for q in questions if not getattr(q, "already_forecasted", False)]

    def close_key(q):
        close_time = getattr(q, "close_time", None)
        # Questions without a close time go last.
        return (close_time is None, close_time.timestamp() if close_time else 0.0)

    fresh.sort(key=close_key)
    return fresh[:max_questions], fresh[max_questions:]
