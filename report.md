# Polymarket strategy lab (pretend money)

Updated 2026-11-07 14:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 170 | 162/170 | +1.3% | +$10.84 | 2 | 261 | too early |
| 2 | sports_underdog | 261 | 60/261 | -10.9% | -$140.47 | 2 | 87 | too early |
| 3 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 103 | too early |
| 4 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 112 | too early |
| 5 | weather_forecast | 10 | 2/10 | -68.6% | -$34.32 | 1 | 177 | too early |
| 6 | safe_no_week | 4 | 4/4 | +4.3% | +$0.87 | 2 | 270 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 103 | 56/103 | +6.9% | +$35.41 | 2 | 329 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$3.27 | -$141.31 | -$10.37 | -$23.43 | -$34.32 | +$0.50 | +$27.98 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Exact Score: AD Tarma 0 - 0 CS Cristal? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Iowa State vs. Baylor -> Iowa State at 0.245 ($5.00)
- 2026-11-07 follow_move: NVIDIA (NVDA) Up or Down on November 9? -> Up at 0.629 ($5.00)
- 2026-11-07 fade_move: NVIDIA (NVDA) Up or Down on November 9? -> Down at 0.435 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Shanghai be 18°C on November 9? -> Yes at 0.159 ($3.27)
- 2026-11-07 safe_no_week: Will the highest temperature in Karachi be 32°C on November 9? -> No at 0.971 ($5.00)
- 2026-11-07 coin_flip: FK Teplice vs. FK Pardubice: O/U 2.5 -> Over at 0.562 ($5.00)
- 2026-11-07 sure_thing: Carrick Rangers vs. Glentoran FC: O/U 5.5 -> Under at 0.943 ($5.00)
- 2026-11-07 sports_underdog: North Carolina vs. UConn -> UConn at 0.276 ($5.00)
- 2026-11-07 follow_move: Will NVIDIA (NVDA) close above $195 on November 9? -> No at 0.845 ($5.00)
- 2026-11-07 fade_move: Will Amazon (AMZN) close above $250 on November 9? -> No at 0.159 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Los Angeles be between 84-85°F on November 9? -> No at 0.818 ($4.30)

## Price gaps seen today

6 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 37 (0 with a problem).
