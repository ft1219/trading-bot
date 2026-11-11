# Polymarket strategy lab (pretend money)

Updated 2026-11-11 14:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 189 | 115/189 | +0.3% | +$2.75 | 6 | 176 | too early |
| 2 | sure_thing | 1280 | 1188/1280 | -0.5% | -$34.27 | 6 | 131 | too early |
| 3 | safe_no_week | 307 | 289/307 | -1.9% | -$28.57 | 6 | 353 | too early |
| 4 | sports_underdog | 995 | 229/995 | -14.3% | -$705.20 | 6 | 39 | too early |
| 5 | fade_move | 212 | 64/212 | -23.0% | -$243.37 | 6 | 193 | too early |
| 6 | weather_forecast | 289 | 145/289 | -25.1% | -$357.00 | 5 | 173 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1342 | 663/1342 | -5.4% | -$359.71 | 6 | 249 | yardstick |

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
| 2026-11-11 | -$7.43 | +$44.43 | -$2.00 | -$80.20 | +$5.95 | -$37.96 | -$22.96 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: S&P 500 (SPY) closes above $755 on November 11? -> Yes at 0.600 ($5.00)
- 2026-11-11 sure_thing: Apple (AAPL) Up or Down on November 11? -> Up at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Seattle be between 60-61°F on November 13? -> No at 0.971 ($5.00)
- 2026-11-11 sports_underdog: Will Oud-Heverlee Leuven Women win on 2026-11-11? -> Yes at 0.198 ($5.00)
- 2026-11-11 fade_move: Will Apple (AAPL) close above $350 on November 11? -> No at 0.162 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Qingdao be 16°C on November 13? -> No at 0.671 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Hyperliquid Up or Down - November 12, 6:40AM-6:45AM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will "Ghost Soldier" Opening Weekend Box Office be between 4m and 5m? -> Yes at 0.482 ($5.00)
- 2026-11-11 sure_thing: Airbnb (ABNB) Up or Down on November 11? -> Down at 0.920 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Panama City be 34°C or higher on November 13? -> No at 0.924 ($5.00)
- 2026-11-11 sports_underdog: Spread: Eintracht Frankfurt (-2.5) -> Eintracht Frankfurt at 0.310 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
