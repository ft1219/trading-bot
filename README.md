# trading-bot

Automated bots that try to earn money from forecasting and markets, built step by step and tested before any real money is used.

The research behind this plan is in [Trading Bot Plan: What Survived the Stress Test](https://claude.ai/code/artifact/c9570a7d-d5f5-414c-a685-3c09856ad310).

| Part | What it does | Money at risk | Status |
| --- | --- | --- | --- |
| [`metaculus-bot/`](metaculus-bot/) | Answers forecasting questions in Metaculus's AI tournaments, which pay prizes to the most accurate bots | None (only AI costs, capped) | Built, waiting for keys |
| Polymarket reward bot | Collects small daily rewards for keeping orders in the book | 20-40 USDT pilot, only after a month of fake-money testing | Not started |

## Setting up the Metaculus bot

You only do this once. Nothing here needs any coding.

1. **Metaculus.** Create an account at [metaculus.com](https://www.metaculus.com). Go to your profile → **Settings → My Forecasting Bots → Create a Bot**, and copy the bot's API token. Then fill in the [participation form](https://forms.gle/aQdYMq9Pisrf1v7d8) (3 required questions).
2. **OpenRouter** (pays for the AI). Create an account at [openrouter.ai](https://openrouter.ai), add $10-20 of credit, and create a key at [openrouter.ai/keys](https://openrouter.ai/keys) with a **credit limit** of $30-50. That limit is the bot's hard spending cap for the season.
3. **AskNews** (news search, free tier). Create an account at [asknews.app](https://asknews.app) and create API credentials (a client ID and a secret).
4. **Give the keys to GitHub, not to anyone in chat.** In this repository open **Settings → Secrets and variables → Actions → New repository secret** and add each of these, names exactly as written:
   - `METACULUS_TOKEN`
   - `OPENROUTER_API_KEY`
   - `ASKNEWS_CLIENT_ID` and `ASKNEWS_SECRET` (or `ASKNEWS_API_KEY` if AskNews gives you a single key)
5. **Practice run.** Open the **Actions** tab → **Metaculus - test on practice questions** → **Run workflow**. After a few minutes, the run should end with "Bot submitted N forecast(s)". These practice questions don't count for prizes.
6. After that, **Metaculus - forecast new questions** runs by itself every 30 minutes.

If a run fails, GitHub emails you; the bot retries on the next run. To pause the bot: **Actions → Metaculus - forecast new questions → ⋯ → Disable workflow**.

## Costs

- **AI:** roughly 1-2 US cents per question with the default model (an estimate until the first live runs report real costs). The OpenRouter key limit caps the season total, and each run stops itself after $1.
- **GitHub:** free. Private repositories get 2,000 free Actions minutes a month; the 30-minute schedule uses roughly 1,500-1,900 of them. If you ever see a minutes warning, change the schedule in `.github/workflows/metaculus-forecast.yaml` to every 40 minutes.
