"""
Runs the bot end to end on made-up questions with the AI calls replaced by
fakes, so nothing touches Metaculus, OpenRouter or AskNews.
"""
import asyncio

import pytest
from forecasting_tools import (
    BinaryPrediction,
    BinaryQuestion,
    GeneralLlm,
    MonetaryCostManager,
)
from forecasting_tools.ai_models.resource_managers.hard_limit_manager import (
    HardLimitExceededError,
)

import main
from bot_config import load_settings


def _questions(count):
    return [
        BinaryQuestion(
            question_text=f"Will test event {i} happen?",
            id_of_post=1000 + i,
            page_url=f"https://www.metaculus.com/questions/{1000 + i}/",
            resolution_criteria="Resolves Yes if it happens.",
            fine_print="",
            background_info="",
            already_forecasted=False,
        )
        for i in range(count)
    ]


def _bot(settings):
    llms = main.build_llms(settings)
    llms["researcher"] = "no_research"
    return main.FallTemplateBot2026(
        research_reports_per_question=1,
        predictions_per_research_report=settings.predictions_per_question,
        use_research_summary_to_forecast=False,
        publish_reports_to_metaculus=False,
        folder_to_save_reports_to=None,
        skip_previously_forecasted_questions=True,
        llms=llms,
    )


@pytest.fixture
def fake_ai(monkeypatch):
    calls = {"invoke": 0}

    async def fake_invoke(self, prompt):
        # Mimic litellm's pre-call hook and its per-call cost tracking.
        MonetaryCostManager.raise_error_if_limit_would_be_reached()
        calls["invoke"] += 1
        MonetaryCostManager.increase_current_usage_in_parent_managers(0.01)
        return "Reasoning... Probability: 37%"

    async def fake_structure_output(*args, **kwargs):
        return BinaryPrediction(prediction_in_decimal=0.37)

    monkeypatch.setattr(GeneralLlm, "invoke", fake_invoke)
    monkeypatch.setattr(main, "structure_output", fake_structure_output)
    return calls


def test_build_llms_turns_on_reasoning_for_the_forecaster():
    llms = main.build_llms(load_settings({}))
    assert llms["default"].litellm_kwargs["extra_body"] == {
        "reasoning": {"enabled": True}
    }
    assert "extra_body" not in llms["parser"].litellm_kwargs
    assert llms["researcher"] == "asknews/news-summaries"


def test_forecasts_every_question_within_budget(fake_ai):
    settings = load_settings({"PREDICTIONS_PER_QUESTION": "5"})
    bot = _bot(settings)
    with MonetaryCostManager(settings.max_cost_per_run_usd) as cost:
        reports = asyncio.run(bot.forecast_questions(_questions(3), return_exceptions=True))
    assert not [r for r in reports if isinstance(r, BaseException)]
    assert [r.prediction for r in reports] == [0.37, 0.37, 0.37]
    # 5 forecasts per question, plus the framework's own summary call.
    assert fake_ai["invoke"] >= 15
    assert cost.current_usage == pytest.approx(fake_ai["invoke"] * 0.01)


def test_cost_cap_stops_ai_calls_once_spent(fake_ai):
    # 0.05 allows five 1-cent calls: one question's worth of forecasts.
    settings = load_settings({"MAX_COST_PER_RUN_USD": "0.05"})
    bot = _bot(settings)
    with MonetaryCostManager(settings.max_cost_per_run_usd):
        reports = asyncio.run(bot.forecast_questions(_questions(4), return_exceptions=True))
    failures = [r for r in reports if isinstance(r, BaseException)]
    assert failures, "the cap should have stopped some questions"
    assert fake_ai["invoke"] <= 6
    assert any(
        isinstance(f, HardLimitExceededError) or "hard limit" in str(f).lower()
        for f in failures
    )


def test_one_tournament_failing_to_load_does_not_block_the_other():
    class FakeClient:
        def get_all_open_questions_from_tournament(self, tournament_id):
            if tournament_id == "minibench":
                raise RuntimeError("between rounds")
            return _questions(2)

    questions, errors = main.collect_questions(FakeClient(), [32813, "minibench"])
    assert len(questions) == 2
    assert len(errors) == 1
