# trading-bot

Automated bots that try to earn money from forecasting and markets, built step by step and tested before any real money is used.

The research behind this plan is in [Trading Bot Plan: What Survived the Stress Test](https://claude.ai/code/artifact/c9570a7d-d5f5-414c-a685-3c09856ad310).

| Part | What it does | Money at risk | Status |
| --- | --- | --- | --- |
| [`metaculus-bot/`](metaculus-bot/) | Answers forecasting questions in Metaculus's AI tournaments, which pay prizes to the most accurate bots | None (only AI costs, capped) | Running since 17 October 2026 |
| [`polymarket-shadow/`](polymarket-shadow/) | Practice mode for a Polymarket reward bot: records, with no money, what keeping small orders in the book would have earned and lost | None (paper trading on public data) | Stopped 3 November 2026: it failed its 14-day check, so there is no real pilot |
| [`polymarket-lab/`](polymarket-lab/) | Strategy lab: tests several Polymarket strategies side by side with pretend money, buying at real asking prices, and ranks them against a fixed pass rule | None (paper trading on public data; free weather data) | Running from November 2026; results on the `polymarket-lab-data` branch, `report.md` |

## Setting up the Metaculus bot

You only do this once. Nothing here needs any coding.

1. **Metaculus.** Create an account at [metaculus.com](https://www.metaculus.com). Go to your profile → **Settings → My Forecasting Bots → Create a Bot**, and copy the bot's API token. Then fill in the [participation form](https://forms.gle/aQdYMq9Pisrf1v7d8) (3 required questions).
2. **OpenRouter** (pays for the AI). Create an account at [openrouter.ai](https://openrouter.ai), add $20 of credit, and create a key at [openrouter.ai/keys](https://openrouter.ai/keys) with a **credit limit** of $40-60. That limit is the bot's hard spending cap for the season.
3. **AskNews** (news search, free tier). Create an account at [asknews.app](https://asknews.app) and create API credentials (a client ID and a secret).
4. **Give the keys to GitHub, not to anyone in chat.** In this repository open **Settings → Secrets and variables → Actions → New repository secret** and add each of these, names exactly as written:
   - `METACULUS_TOKEN`
   - `OPENROUTER_API_KEY`
   - `ASKNEWS_CLIENT_ID` and `ASKNEWS_SECRET` (or `ASKNEWS_API_KEY` if AskNews gives you a single key)
   - Optional: `OPENAI_API_KEY`, an API key from platform.openai.com. When it is set, MiniBench and Metaculus Cup questions use GPT-6 Sol paid from your OpenAI credit instead of DeepSeek.
5. **Check the keys.** Open the **Actions** tab → **Check my keys** → **Run workflow**. The run's summary says which keys work, which are missing, and whether the OpenRouter key has a spending limit. It never shows the keys themselves.
6. **Practice run.** Open the **Actions** tab → **Metaculus - test on practice questions** → **Run workflow**. After a few minutes, the run should end with "Bot submitted N forecast(s)". These practice questions don't count for prizes.
7. **Outside timer.** GitHub's own scheduler never started this workflow on time (since late August 2026 it has been starting scheduled runs hours late or not at all, worst for new repositories), so a free [cron-job.org](https://cron-job.org) account starts it instead:
   - Create a GitHub key with [this pre-filled link](https://github.com/settings/personal-access-tokens/new?name=Bot+timer&expires_in=90&actions=write). Under **Repository access** choose **Only select repositories → trading-bot**, check that **Actions** is **Read and write**, then **Generate token**. Save it as the secret `BOT_TIMER_TOKEN`. It can only manage this repository's Actions runs, not read or change the code.
   - Create a cron-job.org account, then an API key under **Settings** in its console (no IP limit). Save it as the secret `CRONJOB_API_KEY`.
   - Open the **Actions** tab → **Metaculus - set up the outside timer** → **Run workflow**. It checks the GitHub key by starting one run, then creates two cron-job.org jobs that start **Bots - every 40 minutes** every 40 minutes, and prints their next run times.

If a run fails, GitHub emails you; the bot retries on the next run. If cron-job.org cannot start a run, it emails you. To pause the bot, turn off the two "Metaculus bot timer" jobs in the [cron-job.org console](https://console.cron-job.org), or add a repository variable (**Settings → Secrets and variables → Actions → Variables**) named `METACULUS_BOT` with the value `off`. The GitHub key expires after 90 days (mid-January 2027, after this season): make a new one with the same link, replace `BOT_TIMER_TOKEN`, and run the setup workflow again.

## Polymarket practice mode

Nothing to set up: it uses only Polymarket's public data, with no account, keys or money. Once a day it picks the best-paying reward markets. Every 40 minutes it pretends to keep a $20 bid and ask in each, and records the rewards those orders would have earned, the fees Polymarket would have paid back, and what would have been won or lost when prices moved. Markets where nobody else quotes near the middle are shown separately and never count, because paper trading can't tell what would really happen there. Results go to the `polymarket-shadow-data` branch; open `report.md` there to see them.

The report has a go/no-go check fixed in advance: over the first 14 well-covered days, the two pilot markets must average more than $1.50 a day on the cautious estimate. The verdict is taken once, on that 14th day. The report also shows a gentler figure that only lets trades fill the paper orders; the real result is likely between the two. Even if it passes, real trading only starts when you say so, from a Malaysian internet connection, with 20-40 USDT.

**Result:** it failed. Over the 14 well-covered days (18 October to 2 November 2026) the pilot markets averaged -$12.01 a day on the cautious estimate and -$1.89 with trades only, against more than $1.50 needed; 3 of the 14 days were positive. Rewards paid about $5 a day, but prices moving against the paper orders cost more. The recorder was switched off on 3 November 2026; the code and the `polymarket-shadow-data` branch stay for reference.

## Costs

- **AI:** main-tournament questions, where most of the prize money is, use Claude Sonnet 5.5 through OpenRouter, estimated at 15-30 US cents each (the practice run measures it). MiniBench and Metaculus Cup questions use GPT-6 Sol, paid from OpenAI credit, when the optional `OPENAI_API_KEY` secret is set, at about 17 cents each; without it they use DeepSeek V3.2 at about 2-3 cents each. The OpenRouter key limit caps the season total, and **Check my keys** warns when OpenRouter credit runs low. Each run also stops starting new questions once it has spent $3, and every run's log ends with what it spent.
- **GitHub:** free while this repository is public (public repositories get unlimited Actions minutes on standard runners). The timer starts the bots 36 times a day; a quick check first asks Metaculus whether any open question still needs a forecast from the bot, and when none does that job ends in about a minute. The Polymarket strategy lab runs beside it as its own job of 2-4 minutes. If the repository were ever made private again, that would be roughly 3,000-4,000 minutes a month against the 2,000 free ones: pause the lab first (repository variable `POLYMARKET_LAB` = `off`) or change `JOBS` in `metaculus-bot/timer_setup.py` to hourly and run the setup workflow again.
