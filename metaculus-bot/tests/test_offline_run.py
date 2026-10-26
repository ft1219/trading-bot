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


def _bot(settings, budget, forecast_model=None):
    bot = main.make_bot(settings, budget, publish=False, forecast_model=forecast_model)
    bot._llms["researcher"] = "no_research"
    return bot


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


def test_forecaster_waits_up_to_300_seconds_and_no_summary_is_made():
    budget = RunBudget(1.0, 100)
    assert main.build_llms(load_settings({}), budget)["default"].litellm_kwargs["timeout"] == 300
    gemini = main.build_llms(load_settings({}), budget, "openrouter/google/gemini-3.7-flash")
    assert gemini["default"].litellm_kwargs["timeout"] == 300
    bot = main.make_bot(load_settings({}), budget, publish=True)
    assert bot.enable_summarize_research is False
    assert bot.publish_reports_to_metaculus is True


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
    # Only forecasts: no research summary call.
    assert fake_model["calls"] == 15


def test_tournament_questions_use_the_stronger_model_and_minibench_the_cheap_one(fake_model):
    settings = load_settings({})
    budget = RunBudget(settings.max_cost_per_run_usd, settings.max_llm_calls_per_run)
    tournament_bot = _bot(settings, budget, settings.tournament_forecast_model)
    other_bot = _bot(settings, budget)
    questions = _questions(3)
    reports, not_attempted = asyncio.run(
        main.forecast_groups(
            [(tournament_bot, questions[:2]), (other_bot, questions[2:])], 5, budget
        )
    )
    assert not not_attempted
    assert not [r for r in reports if isinstance(r, BaseException)]
    forecaster_models = [k["model"] for k in fake_model["kwargs"] if "extra_body" in k]
    assert forecaster_models.count("openrouter/google/gemini-3.7-flash") == 10
    assert forecaster_models.count("openrouter/deepseek/deepseek-v3.2") == 5
    assert all(
        k["extra_body"] == {"reasoning": {"enabled": True}}
        for k in fake_model["kwargs"]
        if "extra_body" in k
    )


def test_spent_budget_leaves_minibench_for_the_next_run(fake_model):
    settings = load_settings({"MAX_COST_PER_RUN_USD": "0.05", "QUESTIONS_IN_PARALLEL": "1"})
    budget = RunBudget(settings.max_cost_per_run_usd, settings.max_llm_calls_per_run)
    questions = _questions(3)
    reports, not_attempted = asyncio.run(
        main.forecast_groups(
            [
                (_bot(settings, budget, settings.tournament_forecast_model), questions[:1]),
                (_bot(settings, budget), questions[1:]),
            ],
            1,
            budget,
        )
    )
    assert len(reports) == 1
    assert [q.id_of_post for q in not_attempted] == [1001, 1002]


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
    llm = main.build_llms(load_settings({}), budget)["default"]
    llm.allowed_tries = 1
    asyncio.run(llm.invoke("hi"))
    asyncio.run(llm.invoke("hi"))
    with pytest.raises(RunBudgetExceeded, match="spending limit"):
        asyncio.run(llm.invoke("hi"))
    assert fake_model["calls"] == 2


def test_parser_still_reads_paid_forecasts_after_the_limit(fake_model):
    # Forecasts already in flight when the limit is crossed were paid for;
    # refusing their parse calls would throw them away and pay again next run.
    budget = RunBudget(max_cost_usd=0.015, max_calls=100)
    llms = main.build_llms(load_settings({}), budget)
    llms["default"].allowed_tries = 1
    asyncio.run(llms["default"].invoke("hi"))
    asyncio.run(llms["default"].invoke("hi"))
    asyncio.run(llms["parser"].invoke("hi"))
    with pytest.raises(RunBudgetExceeded, match="spending limit"):
        asyncio.run(llms["default"].invoke("hi"))
    assert fake_model["calls"] == 3


def test_parser_still_stops_at_the_call_limit(fake_model):
    budget = RunBudget(max_cost_usd=0.001, max_calls=1)
    llm = main.build_llms(load_settings({}), budget)["parser"]
    llm.allowed_tries = 1
    asyncio.run(llm.invoke("hi"))
    with pytest.raises(RunBudgetExceeded, match="call limit"):
        asyncio.run(llm.invoke("hi"))


def test_calls_that_fail_after_being_sent_still_count(monkeypatch):
    # An empty answer is billed by OpenRouter but raises inside GeneralLlm.
    real_acompletion = litellm.acompletion
    sent = []

    async def empty_acompletion(**kwargs):
        sent.append(1)
        kwargs.pop("extra_body", None)
        return await real_acompletion(mock_response="", **kwargs)

    monkeypatch.setattr(general_llm, "acompletion", empty_acompletion)
    budget = RunBudget(max_cost_usd=100.0, max_calls=100)
    llm = main.build_llms(load_settings({}), budget)["default"]
    with pytest.raises(Exception):
        asyncio.run(llm.invoke("hi"))
    assert len(sent) >= 1
    assert budget.calls == len(sent)
    assert budget.failed_calls == len(sent)


def test_call_limit_stops_model_calls(fake_model):
    budget = RunBudget(max_cost_usd=100.0, max_calls=3)
    llm = main.build_llms(load_settings({}), budget)["parser"]
    llm.allowed_tries = 1
    for _ in range(3):
        asyncio.run(llm.invoke("hi"))
    with pytest.raises(RunBudgetExceeded):
        asyncio.run(llm.invoke("hi"))
    assert fake_model["calls"] == 3


class TournamentClient:
    CURRENT_AI_COMPETITION_ID = 33121
    CURRENT_MINIBENCH_ID = "minibench"
    CURRENT_METACULUS_CUP_ID = "cup"
    OFFSETS = {33121: 0, "minibench": 10, "cup": 20, "bot-testing-area": 30}

    def get_all_open_questions_from_tournament(self, tournament_id):
        return [
            q.model_copy(update={"id_of_post": q.id_of_post + self.OFFSETS[tournament_id]})
            for q in _questions(2)
        ]


@pytest.mark.parametrize(
    "run_mode, strong_posts, cheap_posts",
    [
        ("tournament", [1000, 1001], [1010, 1011]),
        ("metaculus_cup", [], [1020, 1021]),
        ("test_questions", [1030, 1031], []),
    ],
)
def test_each_question_goes_to_the_right_model(run_mode, strong_posts, cheap_posts):
    strong, cheap, errors = main.load_questions(TournamentClient(), run_mode)
    assert not errors
    chosen, _ = main.pick_questions_to_forecast(strong + cheap, max_questions=12)
    chosen_strong, chosen_cheap = main.split_by_model(chosen, strong)
    assert sorted(q.id_of_post for q in chosen_strong) == strong_posts
    assert sorted(q.id_of_post for q in chosen_cheap) == cheap_posts


def test_one_tournament_failing_to_load_does_not_block_the_other():
    class FakeClient:
        def get_all_open_questions_from_tournament(self, tournament_id):
            if tournament_id == "minibench":
                raise RuntimeError("between rounds")
            return _questions(2)

    questions, errors = main.collect_questions(FakeClient(), [33121, "minibench"])
    assert len(questions) == 2
    assert len(errors) == 1
