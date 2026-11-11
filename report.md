# Polymarket strategy lab (pretend money)

Updated 2026-11-11 14:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 189 | 115/189 | +0.3% | +$2.75 | 6 | 172 | too early |
| 2 | sure_thing | 1275 | 1183/1275 | -0.6% | -$35.41 | 6 | 129 | too early |
| 3 | safe_no_week | 307 | 289/307 | -1.9% | -$28.57 | 6 | 351 | too early |
| 4 | sports_underdog | 992 | 228/992 | -14.3% | -$704.44 | 6 | 38 | too early |
| 5 | fade_move | 211 | 64/211 | -22.6% | -$238.37 | 6 | 186 | too early |
| 6 | weather_forecast | 289 | 145/289 | -25.1% | -$357.00 | 5 | 172 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1338 | 661/1338 | -5.4% | -$358.67 | 6 | 245 | yardstick |

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
| 2026-11-11 | -$7.43 | +$43.28 | -$2.00 | -$79.44 | +$10.95 | -$37.96 | -$21.92 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will Apple (AAPL) close above $350 on November 11? -> No at 0.708 ($5.00)
- 2026-11-11 sure_thing: Ethereum Up or Down - November 11, 9:05AM-9:10AM ET -> Down at 0.972 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Kuala Lumpur be 30°C on November 13? -> No at 0.943 ($5.00)
- 2026-11-11 sports_underdog: Florida A&M Rattlers vs. Kansas City Roos -> Florida A&M Rattlers at 0.259 ($5.00)
- 2026-11-11 fade_move: Meta (META) Up or Down on November 11? -> Down at 0.298 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Los Angeles be between 70-71°F on November 13? -> No at 0.632 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: BNB Up or Down - November 11, 9:35PM-9:40PM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will Meta (META) close above $640 on November 11? -> Yes at 0.757 ($5.00)
- 2026-11-11 sure_thing: Dogecoin Up or Down - November 11, 9:05AM-9:10AM ET -> Down at 0.972 ($4.86)
- 2026-11-11 safe_no_week: Will the highest temperature in Atlanta be between 56-57°F on November 13? -> No at 0.973 ($5.00)
- 2026-11-11 sports_underdog: Will Fenerbahce Istanbul win on 2026-11-11? -> Yes at 0.167 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
