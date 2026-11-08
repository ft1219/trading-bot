# Polymarket strategy lab (pretend money)

Updated 2026-11-08 11:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 50 | 48/50 | -0.3% | -$0.81 | 3 | 290 | too early |
| 2 | sure_thing | 465 | 437/465 | -0.4% | -$8.30 | 3 | 222 | too early |
| 3 | sports_underdog | 519 | 116/519 | -14.9% | -$383.29 | 3 | 81 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 122 | too early |
| 5 | weather_forecast | 78 | 37/78 | -25.8% | -$99.73 | 2 | 169 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 131 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 379 | 192/379 | -0.9% | -$16.71 | 3 | 309 | yardstick |

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
| 2026-11-08 | -$2.08 | +$3.42 | -$141.19 |  | +$7.54 | +$1.40 | -$77.07 |
| 2026-11-07 | +$0.90 | -$25.83 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 safe_no_week: Will Silver (XAGUSD) hit (LOW) $45 Week of November 9 2026? -> No at 0.971 ($5.00)
- 2026-11-08 sure_thing: Villarreal CF vs. Getafe CF: Neither team to score first? -> No at 0.962 ($5.00)
- 2026-11-08 sports_underdog: Spread: Brighton & Hove Albion FC (-1.5) -> Brighton & Hove Albion FC at 0.300 ($5.00)
- 2026-11-08 follow_move: Will IShowSpeed win Best IRL Streamer at the 2026 Streamer Awards? -> Yes at 0.827 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Los Angeles be between 82-83°F on November 10? -> No at 0.740 ($5.00)
- 2026-11-08 fade_move: Will Tesla, Inc. (TSLA) hit (LOW) $322.50 Week of November 9 2026? -> Yes at 0.196 ($5.00)
- 2026-11-08 coin_flip: Will Washington Spirit vs. Portland Thorns FC end in a draw? -> No at 0.808 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Denver be between 66-67°F on November 9? -> No at 0.981 ($5.00)
- 2026-11-08 sure_thing: Spread: Halmstads BK (-1.5) -> Djurgardens IF at 0.971 ($5.00)
- 2026-11-08 sports_underdog: Will AC Savoia 1908 win on 2026-11-08? -> Yes at 0.300 ($5.00)
- 2026-11-08 follow_move: Will Meta Platforms, Inc. (META) hit (HIGH) $630 Week of November 9 2026? -> Yes at 0.625 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Madrid be 18°C on November 10? -> No at 0.612 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
