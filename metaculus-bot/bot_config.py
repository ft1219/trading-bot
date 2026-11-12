"""
Our settings for the Metaculus bot: which AI models it uses and how much it
may spend in one run.

Every value can be overridden with an environment variable. In GitHub
Actions these come from repository *variables* (Settings -> Secrets and
variables -> Actions -> Variables), so switching models needs no code change.

The main tournament, where most of the prize money is, gets the strongest
model the budget allows. MiniBench and the Cup use a cheaper one: GPT-6 Sol
when an OPENAI_API_KEY is saved (the owner has free OpenAI credit), otherwise
DeepSeek V3.2.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

# Metaculus runs reference bots on the Fall 2026 tournament with the same
# setup as ours (template bot + AskNews). On 2026-11-10, after 30 scored
# questions each, out of 456: claude-sonnet-5-5-high 33rd (+470),
# gemini-3-8-flash 72nd (+335), gpt-6-sol-high 129th (+169),
# deepseek-3-2-reasoning 312th (-459).
DEFAULT_FORECAST_MODEL = "openrouter/deepseek/deepseek-v3.2"
# Replaces DEFAULT_FORECAST_MODEL when OPENAI_API_KEY is set. Billed to the
# owner's OpenAI credit, not the OpenRouter key. $2 / $10 per million tokens.
OPENAI_FORECAST_MODEL = "openai/gpt-6-sol"
# Main tournament only. $2 / $10 per million tokens on OpenRouter, about 2.7
# times Gemini 3.7 Flash (used from 26 October to November 2026). Prizes go by
# the square of the season score, so the main tournament is where a better
# model pays; MiniBench pays only its top few bots each round.
DEFAULT_TOURNAMENT_FORECAST_MODEL = "openrouter/anthropic/claude-sonnet-5.5"
DEFAULT_PARSER_MODEL = "openrouter/deepseek/deepseek-v3.2"
DEFAULT_RESEARCHER = "asknews/news-summaries"

# Template default is 5 forecasts per question, averaged. Kept as-is.
DEFAULT_PREDICTIONS_PER_QUESTION = 5
# Metaculus releases at most 5 questions at a time; 12 leaves headroom for a
# missed run while still bounding the cost of any single run.
DEFAULT_MAX_QUESTIONS_PER_RUN = 12
# Metaculus releases at most 5 questions at a time; 5 main-tournament questions
# on Claude Sonnet 5.5 plus 5 MiniBench ones on GPT-6 Sol should stay under
# this. The season-wide cap is the spending limit set on the OpenRouter key
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
        forecast_model=_text(
            env,
            "FORECAST_MODEL",
            OPENAI_FORECAST_MODEL
            if (env.get("OPENAI_API_KEY") or "").strip()
            else DEFAULT_FORECAST_MODEL,
        ),
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


def is_claude(model: str) -> bool:
    return model.startswith("openrouter/anthropic/") or model.startswith("anthropic/")


def forecaster_kwargs(settings: BotSettings, model: str | None = None) -> dict:
    """
    Request options for the model that writes the forecasts.

    Claude Sonnet 5.5 always thinks (adaptively) and returns an error for a
    temperature other than its default or for a fixed thinking budget, so it
    gets neither; `effort: high` is its default and matches Metaculus's
    reference bot. OpenAI's GPT-6 models are reasoning models that also take no
    temperature; their reasoning depth is `reasoning_effort`, `high` like the
    reference bots.
    """
    model = model or settings.forecast_model
    if is_claude(model):
        return {
            "temperature": None,
            # Thinking and the written answer share this. Generous, because a
            # cut-off answer fails the whole forecast.
            "max_tokens": 16000,
            "extra_body": {"reasoning": {"effort": "high"}},
        }
    if model.startswith("openai/"):
        # Sent in the request body: litellm 1.80 does not know GPT-6 and drops
        # a top-level reasoning_effort for models it does not know.
        effort = (
            {"extra_body": {"reasoning_effort": "high"}}
            if settings.forecast_reasoning
            else {}
        )
        return {"temperature": None, **effort}
    return {"temperature": 0.3, **reasoning_kwargs(settings, model)}


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
