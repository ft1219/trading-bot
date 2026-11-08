# Polymarket strategy lab (pretend money)

Updated 2026-11-08 02:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 37 | 36/37 | +1.1% | +$1.99 | 3 | 269 | too early |
| 2 | sure_thing | 427 | 400/427 | -0.7% | -$15.01 | 3 | 156 | too early |
| 3 | sports_underdog | 419 | 95/419 | -13.3% | -$276.77 | 3 | 80 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 113 | too early |
| 5 | weather_forecast | 52 | 21/52 | -38.6% | -$100.35 | 2 | 157 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 121 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 298 | 153/298 | +1.3% | +$19.41 | 3 | 286 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$0.72 | -$3.29 | -$34.66 |  | +$6.92 | +$1.40 | -$40.95 |
| 2026-11-07 | +$0.90 | -$25.83 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 safe_no_week: Will the highest temperature in San Francisco be between 74-75°F on November 9? -> No at 0.981 ($5.00)
- 2026-11-08 sure_thing: Persikad Depok vs. Persiku Kudus: O/U 1.5 -> Over at 0.905 ($5.00)
- 2026-11-08 sports_underdog: Spread: Kagoshima United (-1.5) -> Kagoshima United at 0.229 ($5.00)
- 2026-11-08 follow_move: Will Microsoft Corporation (MSFT) hit (LOW) $525 Week of November 9 2026? -> Yes at 0.797 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Sao Paulo be 17°C on November 9? -> No at 0.671 ($5.00)
- 2026-11-08 fade_move: Will Alphabet Inc. (GOOGL) hit (LOW) $280 Week of November 9 2026? -> No at 0.288 ($5.00)
- 2026-11-08 coin_flip: Çorum FK vs. Fenerbahçe SK: Fenerbahçe SK O/U 2.5 -> Under at 0.723 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Houston be between 62-63°F on November 9? -> No at 0.952 ($5.00)
- 2026-11-08 sure_thing: Exact Score: Sportivo Trinidense 0 - 0 Sportivo Ameliano? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Will Vanraure Hachinohe FC win on 2026-11-07? -> Yes at 0.341 ($5.00)
- 2026-11-08 follow_move: Will Alphabet Inc. (GOOGL) hit (LOW) $280 Week of November 9 2026? -> Yes at 0.767 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Karachi be 35°C on November 9? -> No at 0.642 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
