# trading-bot

Automated bots that try to earn money from forecasting and markets, built step by step and tested before any real money is used.

The research behind this plan is in [Trading Bot Plan: What Survived the Stress Test](https://claude.ai/code/artifact/c9570a7d-d5f5-414c-a685-3c09856ad310).

| Part | What it does | Money at risk | Status |
| --- | --- | --- | --- |
| [`metaculus-bot/`](metaculus-bot/) | Answers forecasting questions in Metaculus's AI tournaments, which pay prizes to the most accurate bots | None (only AI costs, capped) | Built, waiting for keys |
| [`polymarket-shadow/`](polymarket-shadow/) | Practice mode for a Polymarket reward bot: records, with no money, what keeping small orders in the book would have earned and lost | None (paper trading on public data) | Built; a real 20-40 USDT pilot only if it passes the check below and you say go |

## Setting up the Metaculus bot

You only do this once. Nothing here needs any coding.

1. **Metaculus.** Create an account at [metaculus.com](https://www.metaculus.com). Go to your profile → **Settings → My Forecasting Bots → Create a Bot**, and copy the bot's API token. Then fill in the [participation form](https://forms.gle/aQdYMq9Pisrf1v7d8) (3 required questions).
2. **OpenRouter** (pays for the AI). Create an account at [openrouter.ai](https://openrouter.ai), add $10-20 of credit, and create a key at [openrouter.ai/keys](https://openrouter.ai/keys) with a **credit limit** of $30-50. That limit is the bot's hard spending cap for the season.
3. **AskNews** (news search, free tier). Create an account at [asknews.app](https://asknews.app) and create API credentials (a client ID and a secret).
4. **Give the keys to GitHub, not to anyone in chat.** In this repository open **Settings → Secrets and variables → Actions → New repository secret** and add each of these, names exactly as written:
   - `METACULUS_TOKEN`
   - `OPENROUTER_API_KEY`
   - `ASKNEWS_CLIENT_ID` and `ASKNEWS_SECRET` (or `ASKNEWS_API_KEY` if AskNews gives you a single key)
5. **Check the keys.** Open the **Actions** tab → **Check my keys** → **Run workflow**. The run's summary says which keys work, which are missing, and whether the OpenRouter key has a spending limit. It never shows the keys themselves.
6. **Practice run.** Open the **Actions** tab → **Metaculus - test on practice questions** → **Run workflow**. After a few minutes, the run should end with "Bot submitted N forecast(s)". These practice questions don't count for prizes.
7. After that, **Bots - every 40 minutes** runs by itself.

If a run fails, GitHub emails you; the bot retries on the next run. To pause both bots: **Actions → Bots - every 40 minutes → ⋯ → Disable workflow**. To pause only one, add a repository variable (**Settings → Secrets and variables → Actions → Variables**) named `METACULUS_BOT` or `POLYMARKET_PRACTICE` with the value `off`.

## Polymarket practice mode

Nothing to set up: it uses only Polymarket's public data, with no account, keys or money. Every 40 minutes it picks the best-paying reward markets, pretends to keep a $20 bid and ask in each, and records the rewards those orders would have earned, the fees Polymarket would have paid back, and what would have been won or lost when prices moved. Results go to the `polymarket-shadow-data` branch; open `report.md` there to see them.

The report ends each day with a go/no-go check fixed in advance: after at least 14 full days, the two pilot markets must average more than $1.50 a day on the cautious estimate. Even if it passes, real trading only starts when you say so, from a Malaysian internet connection, with 20-40 USDT.

## Costs

- **AI:** roughly 1-2 US cents per question with the default model (an estimate until the first live runs report real costs). The OpenRouter key limit caps the season total. Each run also stops starting new questions once it has spent $1, and every run's log ends with what it spent.
- **GitHub:** free. Private repositories get 2,000 free Actions minutes a month. The schedule runs 36 times a day; a quick check first asks Metaculus whether any open question still needs a forecast from the bot, and when none does the run ends in under a minute. That is about 1,100 minutes a month plus the runs that actually forecast. The Polymarket practice step runs inside the same minute. If GitHub warns about minutes, the workflow file says how to switch to hourly runs.
