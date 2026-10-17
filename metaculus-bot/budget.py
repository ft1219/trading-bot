"""
Per-run AI spending limit, enforced in our own code.

forecasting-tools' MonetaryCostManager cannot stop a call: its check runs
inside a litellm logging callback, and litellm catches and logs exceptions
raised there. So every model call goes through BudgetedLlm, which checks the
run budget before the call (raising RunBudgetExceeded, which does reach the
bot) and records the call's real cost afterwards.

A few questions are forecast at a time, so a run can overshoot the limit by
the calls already in flight when it is reached: a few cents with the default
model. The season-wide hard cap is the OpenRouter key's own limit.
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

    @property
    def exhausted(self) -> bool:
        return self.spent_usd >= self.max_cost_usd or self.calls >= self.max_calls

    def check(self) -> None:
        if self.spent_usd >= self.max_cost_usd:
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


class BudgetedLlm(GeneralLlm):
    """A GeneralLlm that refuses to call the model once the run budget is spent."""

    def __init__(self, *args, budget: RunBudget, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._budget = budget

    async def _mockable_direct_call_to_model(self, prompt):
        self._budget.check()
        response = await super()._mockable_direct_call_to_model(prompt)
        # response.cost is the price litellm attached to this one call; the
        # library's own cost managers count each call twice.
        self._budget.record(getattr(response, "cost", None))
        return response
