# Metaculus forecasting bot

Forecasts on open questions in the Metaculus Fall 2026 FutureEval bot tournament and MiniBench, and submits them through the Metaculus API.

Based on Metaculus's official [metac-bot-template](https://github.com/Metaculus/metac-bot-template) at commit `096cb20`, imported unchanged in the first commit so the history shows only our changes:

- `bot_config.py`: models and limits, each overridable with an environment variable (repository variable in Actions).
- `main.py`: pins the models instead of the template's GPT-4o defaults (a stronger one for the main tournament, a cheaper one for MiniBench), forecasts the soonest-closing questions first up to `MAX_QUESTIONS_PER_RUN`, a few at a time, stops once the run budget is spent, adds `--dry-run`, and exits non-zero when any question fails or is skipped so the Actions run shows red.
- `budget.py`: the per-run spending and call limits. forecasting-tools' own `MonetaryCostManager` cannot stop a call (litellm swallows the exception its callback raises), so `BudgetedLlm` checks the budget before every model call and records each call's real cost once. Calls that fail after being sent still count toward the call limit. The parser, which only reads answers already paid for, keeps working past the spending limit so those forecasts are not thrown away.
- `precheck.py`: standard-library check run before installing anything. When no open question is waiting for a first forecast from the bot, the scheduled job ends early. Errors and unfamiliar responses count as "something to forecast", so it can never cause a missed question.
- `timer_setup.py`: creates or updates the two cron-job.org jobs that start the forecasting workflow every 40 minutes through its dispatch endpoint, because GitHub's own `schedule` trigger fired hours late and irregularly for this repository. Run it with the **Metaculus - set up the outside timer** workflow.
- `bot_helpers.py`: the setup check also requires `OPENROUTER_API_KEY` and AskNews keys, so the bot never falls back to a different, unbudgeted provider. Blank key variables (GitHub's value for a secret that was never created) are removed at startup; a blank `ASKNEWS_API_KEY` would otherwise override a valid client ID and secret.

## Settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `TOURNAMENT_FORECAST_MODEL` | `openrouter/google/gemini-3.7-flash` | Model that writes the forecasts for the main tournament and the practice run. Scores about 11.8 on Metaculus's FutureEval model leaderboard against 6.9 for DeepSeek 3.2, at roughly $0.08-0.20 a question. |
| `FORECAST_MODEL` | `openrouter/deepseek/deepseek-v3.2` | Model that writes the forecasts for MiniBench and the Metaculus Cup. With AskNews this matches Metaculus's `metac-deepseek-3-2-reasoning+asknews` baseline (5th of the Metaculus baselines, Spring 2026). |
| `FORECAST_REASONING` | `true` | Turns on the model's reasoning mode on OpenRouter. |
| `PARSER_MODEL` | `openrouter/deepseek/deepseek-v3.2` | Model that turns the forecast text into numbers. |
| `RESEARCHER` | `asknews/news-summaries` | News research for each question. |
| `PREDICTIONS_PER_QUESTION` | `5` | Forecasts averaged per question. |
| `MAX_QUESTIONS_PER_RUN` | `12` | Questions handled per run; the rest wait for the next run. |
| `MAX_COST_PER_RUN_USD` | `3.00` | AI spending limit per run, checked before every call. Must be above 0. |
| `MAX_LLM_CALLS_PER_RUN` | `400` | Backstop limit on AI calls per run, for models whose price litellm does not know. |
| `QUESTIONS_IN_PARALLEL` | `5` | Questions forecast at once. Calls already in flight when the limit is reached still finish, so this bounds the overshoot. |

## Running locally

```bash
cp .env.template .env   # fill in the keys
poetry install
poetry run python main.py --mode test_questions --dry-run
poetry run python -m pip install pytest && poetry run python -m pytest -q tests
```
