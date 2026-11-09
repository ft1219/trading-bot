# Polymarket strategy lab (pretend money)

Updated 2026-11-09 22:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 913 | 844/913 | -1.4% | -$64.98 | 4 | 137 | too early |
| 2 | safe_no_week | 183 | 171/183 | -2.8% | -$26.00 | 4 | 304 | too early |
| 3 | follow_move | 121 | 72/121 | -5.5% | -$33.36 | 4 | 145 | too early |
| 4 | sports_underdog | 775 | 170/775 | -17.6% | -$677.06 | 4 | 74 | too early |
| 5 | weather_forecast | 184 | 93/184 | -23.6% | -$214.59 | 3 | 148 | too early |
| 6 | fade_move | 139 | 40/139 | -37.0% | -$257.29 | 4 | 156 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 897 | 454/897 | -2.6% | -$117.53 | 4 | 214 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | follow_move | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-09 | -$0.56 | -$7.35 | +$23.36 | -$172.11 | -$73.11 | -$73.83 | +$31.11 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Ethereum Up or Down - November 9, 5PM ET -> Up at 0.963 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Istanbul be 19°C on November 11? -> No at 0.959 ($5.00)
- 2026-11-09 follow_move: Will there be ≤6 earthquakes of 5.5 or above magnitude worldwide? -> Yes at 0.392 ($5.00)
- 2026-11-09 sports_underdog: Matsuyama: Shunsuke Nakagawa vs David Jorda Sanchis -> Shunsuke Nakagawa at 0.218 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Chongqing be 17°C on November 11? -> No at 0.632 ($5.00)
- 2026-11-09 fade_move: Will there be ≤6 earthquakes of 5.5 or above magnitude worldwide? -> No at 0.665 ($5.00)
- 2026-11-09 coin_flip: Will Microsoft (MSFT) close above $550 on November 10? -> Yes at 0.319 ($5.00)
- 2026-11-09 sure_thing: Dogecoin Up or Down - November 9, 5PM ET -> Up at 0.935 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Moscow be 5°C on November 11? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will the price of XRP be above $1.10 on November 15? -> No at 0.577 ($5.00)
- 2026-11-09 sports_underdog: Rangers vs. Oilers: O/U 4.5 -> Under at 0.198 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Manila be 32°C on November 11? -> No at 0.592 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (11 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
