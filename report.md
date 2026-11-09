# Polymarket strategy lab (pretend money)

Updated 2026-11-09 23:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 921 | 852/921 | -1.4% | -$62.78 | 4 | 136 | too early |
| 2 | safe_no_week | 189 | 177/189 | -2.5% | -$23.93 | 4 | 301 | too early |
| 3 | follow_move | 126 | 74/126 | -7.3% | -$45.66 | 4 | 140 | too early |
| 4 | sports_underdog | 780 | 171/780 | -17.7% | -$686.95 | 4 | 70 | too early |
| 5 | weather_forecast | 189 | 96/189 | -23.4% | -$217.88 | 3 | 144 | too early |
| 6 | fade_move | 145 | 43/145 | -34.5% | -$250.45 | 4 | 150 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 904 | 457/904 | -2.7% | -$122.15 | 4 | 215 | yardstick |

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
| 2026-11-09 | +$1.64 | -$5.28 | +$11.06 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: WTI Crude Oil (WTI) closes above $91 on November 10? -> No at 0.971 ($5.00)
- 2026-11-09 safe_no_week: Will "BbY WOW - KAROL G, Judeline, rusowsky" be the #1 song this week? -> Yes at 0.962 ($5.00)
- 2026-11-09 follow_move: Will there be ≤6 earthquakes of 5.5 or above magnitude worldwide? -> Yes at 0.392 ($5.00)
- 2026-11-09 sports_underdog: Spurs vs. Suns -> Suns at 0.249 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Munich be 12°C on November 11? -> No at 0.701 ($5.00)
- 2026-11-09 fade_move: Will there be ≤6 earthquakes of 5.5 or above magnitude worldwide? -> No at 0.665 ($5.00)
- 2026-11-09 coin_flip: Dogecoin Up or Down - November 10, 5PM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: XRP Up or Down - November 9, 6:15PM-6:30PM ET -> Down at 0.830 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Munich be 11°C on November 11? -> No at 0.934 ($5.00)
- 2026-11-09 follow_move: Will the price of XRP be above $1.10 on November 15? -> No at 0.577 ($5.00)
- 2026-11-09 sports_underdog: Matsuyama: Shunsuke Nakagawa vs David Jorda Sanchis -> Shunsuke Nakagawa at 0.218 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Chongqing be 17°C on November 11? -> No at 0.632 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (12 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
