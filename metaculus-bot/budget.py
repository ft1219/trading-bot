"""
Per-run AI spending limit, enforced in our own code.

forecasting-tools' MonetaryCostManager cannot stop a call: its check runs
inside a litellm logging callback, and litellm catches and logs exceptions
raised there. So every model call goes through BudgetedLlm, which checks the
run budget before the call (raising RunBudgetExceeded, which does reach the
bot) and records the call's real cost afterwards.

A few questions are forecast at a time, so a run can overshoot the limit by
the calls already in flight when it is reached: up to about a dollar with
five main-tournament questions on Gemini. The parser that reads those
forecasts' answers is exempt from the spending limit (it costs a fraction of
a cent and only reads answers already paid for), so a run that crosses the
limit still publishes the forecasts it paid for. The season-wide hard cap is
the OpenRouter key's own limit.
"""
from __future__ import annotations

from forecasting_tools import GeneralLlm


class RunBudgetExceeded(RuntimeError):
    pass


class RunBudget:
    def __init__(self, max_cost_usd: float, max_calls: int) -> None:
        self.max_cost_usd = max_cost_usd
        self.max_calls = max_calls
        self.spent_usd = 0.0
        self.calls = 0
        self.calls_without_cost = 0
        self.failed_calls = 0

    @property
    def exhausted(self) -> bool:
        return self.spent_usd >= self.max_cost_usd or self.calls >= self.max_calls

    def check(self, enforce_spending_limit: bool = True) -> None:
        if enforce_spending_limit and self.spent_usd >= self.max_cost_usd:
            raise RunBudgetExceeded(
                f"Run spending limit reached: ${self.spent_usd:.4f} of "
                f"${self.max_cost_usd:.2f}. Remaining questions wait for the next run."
            )
        if self.calls >= self.max_calls:
            raise RunBudgetExceeded(
                f"Run call limit reached: {self.calls} of {self.max_calls} AI calls. "
                "Remaining questions wait for the next run."
            )

    def record(self, cost_usd: float | None) -> None:
        self.calls += 1
        if not cost_usd:
            # litellm could not price the call (unknown model). The call limit
            # still bounds the run.
            self.calls_without_cost += 1
            return
        self.spent_usd += cost_usd

    def record_failure(self) -> None:
        # The call was sent but raised (a timeout, or an empty answer that
        # OpenRouter still billed). Its cost is unknown; counting it keeps
        # the call limit honest when a model keeps failing.
        self.calls += 1
        self.failed_calls += 1


class BudgetedLlm(GeneralLlm):
    """A GeneralLlm that refuses to call the model once the run budget is spent."""

    def __init__(
        self, *args, budget: RunBudget, enforce_spending_limit: bool = True, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._budget = budget
        self._enforce_spending_limit = enforce_spending_limit

    async def _mockable_direct_call_to_model(self, prompt):
        self._budget.check(self._enforce_spending_limit)
        try:
            response = await super()._mockable_direct_call_to_model(prompt)
        except Exception:
            self._budget.record_failure()
            raise
        # response.cost is the price litellm attached to this one call; the
        # library's own cost managers count each call twice.
        self._budget.record(getattr(response, "cost", None))
        return response
