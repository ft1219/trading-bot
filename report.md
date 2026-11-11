# Polymarket strategy lab (pretend money)

Updated 2026-11-11 00:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 183 | 112/183 | +1.3% | +$11.70 | 6 | 141 | too early |
| 2 | sure_thing | 1182 | 1094/1182 | -1.3% | -$76.61 | 6 | 104 | too early |
| 3 | safe_no_week | 275 | 259/275 | -1.9% | -$25.98 | 6 | 328 | too early |
| 4 | sports_underdog | 941 | 217/941 | -13.9% | -$651.94 | 6 | 46 | too early |
| 5 | weather_forecast | 261 | 131/261 | -25.1% | -$321.62 | 5 | 146 | too early |
| 6 | fade_move | 202 | 61/202 | -25.2% | -$254.32 | 6 | 154 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1191 | 583/1191 | -6.0% | -$356.80 | 6 | 224 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-11 | +$1.52 | +$2.09 | +$0.59 | -$26.94 | -$2.57 | -$5.00 | -$20.05 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | -$101.16 | +$1.13 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Will "Cuffem's Team" win Nozempic 2? -> No at 0.701 ($5.00)
- 2026-11-11 sure_thing: Saint Peter's Peacocks vs. South Carolina Gamecocks -> South Carolina Gamecocks at 0.971 ($5.00)
- 2026-11-11 safe_no_week: Will MrBeast's next video get between 35 and 40 million views on day 1? -> No at 0.924 ($5.00)
- 2026-11-11 sports_underdog: Arizona State Sun Devils vs. UNLV Runnin' Rebels (W) -> UNLV Runnin' Rebels at 0.310 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Dallas be between 60-61°F on November 11? -> No at 0.665 ($5.00)
- 2026-11-10 fade_move: Will "Cuffem's Team" win Nozempic 2? -> Yes at 0.331 ($5.00)
- 2026-11-11 coin_flip: BNB Up or Down - November 11, 5:05AM-5:10AM ET -> Down at 0.527 ($5.00)
- 2026-11-10 follow_move: Will Donald Trump post 200+ Truth Social posts from November 10 to November 17, 2026? -> No at 0.856 ($5.00)
- 2026-11-11 sure_thing: Lightning vs. Sabres: O/U 3.5 -> Over at 0.914 ($5.00)
- 2026-11-10 safe_no_week: Will Google have the third highest OpenRouter market share the week of November 9? -> Yes at 0.962 ($5.00)
- 2026-11-11 sports_underdog: Predators vs. Kings: O/U 4.5 -> Under at 0.229 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Sao Paulo be 28°C on November 12? -> No at 0.715 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
