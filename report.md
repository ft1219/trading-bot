# Polymarket strategy lab (pretend money)

Updated 2026-11-07 17:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 19 | 19/19 | +4.6% | +$4.35 | 2 | 273 | too early |
| 2 | sure_thing | 217 | 209/217 | +2.2% | +$23.75 | 2 | 254 | too early |
| 3 | sports_underdog | 311 | 67/311 | -16.1% | -$248.64 | 2 | 77 | too early |
| 4 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 110 | too early |
| 5 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 120 | too early |
| 6 | weather_forecast | 31 | 9/31 | -55.6% | -$86.16 | 1 | 163 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 137 | 75/137 | +8.5% | +$57.72 | 2 | 335 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | +$3.98 | +$9.64 | -$249.48 | -$10.37 | -$23.43 | -$86.16 | +$50.29 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will Microsoft (MSFT) finish week of November 9 above $500? -> Yes at 0.942 ($5.00)
- 2026-11-07 sure_thing: Spread: PSS Sleman (-1.5) -> Bhayangkara Presisi Lampung FC at 0.905 ($5.00)
- 2026-11-07 sports_underdog: Spread: São Bernardo FC (-1.5) -> São Bernardo FC at 0.187 ($5.00)
- 2026-11-07 follow_move: Will the price of XRP be above $1.20 on November 13? -> No at 0.724 ($5.00)
- 2026-11-07 fade_move: Will the price of Bitcoin be above $80,000 on November 13? -> Yes at 0.147 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in London be 5°C on November 9? -> No at 0.652 ($5.00)
- 2026-11-07 coin_flip: Will KFC Komárno win on 2026-11-08? -> Yes at 0.592 ($5.00)
- 2026-11-07 safe_no_week: Will the price of Ethereum be above $2,500 on November 14? -> No at 0.972 ($5.00)
- 2026-11-07 sure_thing: Exact Score: CA Boca Juniors 0 - 0 CSyD Defensa y Justicia? -> No at 0.952 ($5.00)
- 2026-11-07 sports_underdog: UNCW Seahawks vs. East Carolina Pirates -> East Carolina Pirates at 0.361 ($5.00)
- 2026-11-07 follow_move: Will the price of Ethereum be between $2,100 and $2,200 on November 12? -> No at 0.802 ($5.00)
- 2026-11-07 fade_move: Will the price of Ethereum be between $2,000 and $2,100 on November 13? -> Yes at 0.127 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
