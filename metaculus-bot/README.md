# Metaculus forecasting bot

Forecasts on open questions in the Metaculus Fall 2026 FutureEval bot tournament and MiniBench, and submits them through the Metaculus API.

Based on Metaculus's official [metac-bot-template](https://github.com/Metaculus/metac-bot-template) at commit `096cb20`, imported unchanged in the first commit so the history shows only our changes:

- `bot_config.py`: models and limits, each overridable with an environment variable (repository variable in Actions).
- `main.py`: pins the models instead of the template's GPT-4o defaults, forecasts the soonest-closing questions first up to `MAX_QUESTIONS_PER_RUN`, wraps each run in a `MonetaryCostManager` hard limit, adds `--dry-run`, and exits non-zero when any question fails so the Actions run shows red.
- `bot_helpers.py`: the setup check also requires `OPENROUTER_API_KEY` and AskNews keys, so the bot never falls back to a different, unbudgeted provider.

## Settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `FORECAST_MODEL` | `openrouter/deepseek/deepseek-v3.2` | Model that writes the forecasts. With AskNews this matches Metaculus's `metac-deepseek-3-2-reasoning+asknews` baseline (5th of the Metaculus baselines, Spring 2026). |
| `FORECAST_REASONING` | `true` | Turns on the model's reasoning mode on OpenRouter. |
| `PARSER_MODEL` | `openrouter/deepseek/deepseek-v3.2` | Model that turns the forecast text into numbers. |
| `RESEARCHER` | `asknews/news-summaries` | News research for each question. |
| `PREDICTIONS_PER_QUESTION` | `5` | Forecasts averaged per question. |
| `MAX_QUESTIONS_PER_RUN` | `12` | Questions handled per run; the rest wait for the next run. |
| `MAX_COST_PER_RUN_USD` | `1.00` | Hard AI spending limit per run. Must be above 0. |

## Running locally

```bash
cp .env.template .env   # fill in the keys
poetry install
poetry run python main.py --mode test_questions --dry-run
poetry run python -m pip install pytest && poetry run python -m pytest -q tests
```
