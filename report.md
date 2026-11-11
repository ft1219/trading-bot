# Polymarket strategy lab (pretend money)

Updated 2026-11-11 21:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 222 | 137/222 | +1.8% | +$19.88 | 6 | 158 | too early |
| 2 | sure_thing | 1343 | 1249/1343 | -0.3% | -$22.13 | 6 | 137 | too early |
| 3 | safe_no_week | 344 | 322/344 | -2.4% | -$42.07 | 6 | 342 | too early |
| 4 | sports_underdog | 1029 | 233/1029 | -15.1% | -$775.35 | 6 | 52 | too early |
| 5 | fade_move | 249 | 73/249 | -24.1% | -$299.39 | 6 | 170 | too early |
| 6 | weather_forecast | 313 | 157/313 | -25.3% | -$389.95 | 5 | 157 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1412 | 699/1412 | -5.3% | -$374.87 | 6 | 249 | yardstick |

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
| 2026-11-11 | +$9.69 | +$56.57 | -$15.49 | -$150.35 | -$50.06 | -$70.91 | -$38.12 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Bitcoin Up or Down on November 12? -> Up at 0.656 ($5.00)
- 2026-11-11 sure_thing: San Marino to score first vs. Belarus? -> No at 0.924 ($5.00)
- 2026-11-11 safe_no_week: Will "Choosin' Texas - Ella Langley" be the Billboard Hot 100 #2 song for the week of November 21? -> No at 0.985 ($5.00)
- 2026-11-11 sports_underdog: Wizards vs. Pacers: O/U 236.5 -> Over at 0.331 ($5.00)
- 2026-11-11 fade_move: Bitcoin Up or Down on November 12? -> Down at 0.386 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in San Francisco be between 62-63°F on November 13? -> No at 0.498 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Ethereum Up or Down - November 11, 6:50PM-6:55PM ET -> Down at 0.527 ($5.00)
- 2026-11-11 follow_move: Will NYC get 1.50" or more of rain November 12 to 15? -> No at 0.681 ($5.00)
- 2026-11-11 sure_thing: Albania vs. Finland: Neither team to score first? -> No at 0.905 ($5.00)
- 2026-11-11 safe_no_week: Will "Black Doves: Season 2" be the top global Netflix show this week? -> No at 0.981 ($5.00)
- 2026-11-11 sports_underdog: Cavaliers vs. Knicks: O/U 229.5 -> Over at 0.351 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 36 position(s) still open more than 3 days after their market ended
