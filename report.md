# Polymarket strategy lab (pretend money)

Updated 2026-11-11 22:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 222 | 137/222 | +1.8% | +$19.88 | 6 | 158 | too early |
| 2 | sure_thing | 1352 | 1258/1352 | -0.3% | -$20.02 | 6 | 136 | too early |
| 3 | safe_no_week | 346 | 324/346 | -2.4% | -$41.55 | 6 | 341 | too early |
| 4 | sports_underdog | 1037 | 234/1037 | -15.3% | -$790.06 | 6 | 52 | too early |
| 5 | fade_move | 249 | 73/249 | -24.1% | -$299.39 | 6 | 170 | too early |
| 6 | weather_forecast | 315 | 158/315 | -25.3% | -$392.04 | 5 | 155 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1420 | 704/1420 | -5.2% | -$369.39 | 6 | 249 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-11 | +$9.69 | +$58.68 | -$14.97 | -$165.06 | -$50.06 | -$73.00 | -$32.64 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Bitcoin Up or Down on November 12? -> Up at 0.656 ($5.00)
- 2026-11-11 sure_thing: Will AD Pasto win on 2026-11-12? -> No at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will Cisco (CSCO) Q1 Networking revenue be above $10.4B? -> Yes at 0.962 ($5.00)
- 2026-11-11 sports_underdog: Coppin State Eagles vs. Hofstra Pride (W) -> Coppin State Eagles at 0.270 ($5.00)
- 2026-11-11 fade_move: Bitcoin Up or Down on November 12? -> Down at 0.386 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in San Francisco be between 62-63°F on November 13? -> No at 0.498 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: ZCash Up or Down - November 12, 12:00PM-12:05PM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will NYC get 1.50" or more of rain November 12 to 15? -> No at 0.681 ($5.00)
- 2026-11-11 sure_thing: Sudan leading at halftime? -> No at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will "Choosin' Texas - Ella Langley" be the Billboard Hot 100 #2 song for the week of November 21? -> No at 0.985 ($5.00)
- 2026-11-11 sports_underdog: Nuggets vs. Grizzlies: O/U 222.5 -> Under at 0.351 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 35 (35 with a problem).
Latest problem: 36 position(s) still open more than 3 days after their market ended
