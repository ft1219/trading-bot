"""
Runs the bot end to end on made-up questions with the network calls replaced,
so nothing touches Metaculus, OpenRouter or AskNews.

The model call is stubbed at litellm's `acompletion`, below forecasting-tools,
so the real GeneralLlm/BudgetedLlm code (and its cost accounting) runs.
"""
import asyncio

import litellm
import pytest
from forecasting_tools import BinaryPrediction, BinaryQuestion
from forecasting_tools.ai_models import general_llm

import main
from bot_config import load_settings
from budget import RunBudget, RunBudgetExceeded

COST_PER_CALL = 0.01


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


def _bot(settings, budget):
    llms = main.build_llms(settings, budget)
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
def fake_model(monkeypatch):
    seen = {"calls": 0, "kwargs": []}
    real_acompletion = litellm.acompletion

    async def fake_acompletion(**kwargs):
        seen["calls"] += 1
        seen["kwargs"].append(dict(kwargs))
        kwargs.pop("extra_body", None)
        response = await real_acompletion(
            mock_response="Reasoning... Probability: 37%", **kwargs
        )
        response._hidden_params["response_cost"] = COST_PER_CALL
        return response

    async def fake_structure_output(*args, **kwargs):
        return BinaryPrediction(prediction_in_decimal=0.37)

    monkeypatch.setattr(general_llm, "acompletion", fake_acompletion)
    monkeypatch.setattr(main, "structure_output", fake_structure_output)
    return seen


def test_build_llms_turns_on_reasoning_for_the_forecaster():
    llms = main.build_llms(load_settings({}), RunBudget(1.0, 100))
    assert llms["default"].litellm_kwargs["extra_body"] == {
        "reasoning": {"enabled": True}
    }
    assert "extra_body" not in llms["parser"].litellm_kwargs
    assert llms["researcher"] == "asknews/news-summaries"


def test_forecasts_every_question_and_counts_real_cost_once(fake_model):
    settings = load_settings({"PREDICTIONS_PER_QUESTION": "5"})
    budget = RunBudget(settings.max_cost_per_run_usd, settings.max_llm_calls_per_run)
    bot = _bot(settings, budget)
    reports = asyncio.run(bot.forecast_questions(_questions(3), return_exceptions=True))
    assert not [r for r in reports if isinstance(r, BaseException)]
    assert [r.prediction for r in reports] == [0.37, 0.37, 0.37]
    assert budget.calls == fake_model["calls"]
    assert budget.spent_usd == pytest.approx(fake_model["calls"] * COST_PER_CALL)
    forecaster_calls = [k for k in fake_model["kwargs"] if "extra_body" in k]
    assert len(forecaster_calls) == 15


def test_spending_limit_stops_the_run_between_batches(fake_model):
    settings = load_settings(
        {"MAX_COST_PER_RUN_USD": "0.05", "QUESTIONS_IN_PARALLEL": "1"}
    )
    budget = RunBudget(settings.max_cost_per_run_usd, settings.max_llm_calls_per_run)
    bot = _bot(settings, budget)
    reports, not_attempted = asyncio.run(
        main.forecast_in_batches(bot, _questions(4), 1, budget)
    )
    # The first question's calls start before the limit is reached and finish;
    # after that the run stops instead of starting more questions.
    assert len(reports) == 1
    assert [q.id_of_post for q in not_attempted] == [1001, 1002, 1003]
    assert budget.spent_usd >= 0.05
    assert fake_model["calls"] == budget.calls


def test_a_call_starting_after_the_limit_is_refused(fake_model):
    budget = RunBudget(max_cost_usd=0.015, max_calls=100)
    llm = main.build_llms(load_settings({}), budget)["parser"]
    llm.allowed_tries = 1
    asyncio.run(llm.invoke("hi"))
    asyncio.run(llm.invoke("hi"))
    with pytest.raises(RunBudgetExceeded, match="spending limit"):
        asyncio.run(llm.invoke("hi"))
    assert fake_model["calls"] == 2


def test_call_limit_stops_model_calls(fake_model):
    budget = RunBudget(max_cost_usd=100.0, max_calls=3)
    llm = main.build_llms(load_settings({}), budget)["parser"]
    llm.allowed_tries = 1
    for _ in range(3):
        asyncio.run(llm.invoke("hi"))
    with pytest.raises(RunBudgetExceeded):
        asyncio.run(llm.invoke("hi"))
    assert fake_model["calls"] == 3


def test_one_tournament_failing_to_load_does_not_block_the_other():
    class FakeClient:
        def get_all_open_questions_from_tournament(self, tournament_id):
            if tournament_id == "minibench":
                raise RuntimeError("between rounds")
            return _questions(2)

    questions, errors = main.collect_questions(FakeClient(), [33121, "minibench"])
    assert len(questions) == 2
    assert len(errors) == 1
