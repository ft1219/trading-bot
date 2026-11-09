# Polymarket strategy lab (pretend money)

Updated 2026-11-09 18:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 874 | 807/874 | -1.5% | -$66.54 | 4 | 128 | too early |
| 2 | safe_no_week | 160 | 150/160 | -2.6% | -$20.79 | 4 | 313 | too early |
| 3 | follow_move | 98 | 56/98 | -9.2% | -$44.93 | 4 | 163 | too early |
| 4 | sports_underdog | 754 | 167/754 | -16.5% | -$617.37 | 4 | 58 | too early |
| 5 | weather_forecast | 172 | 87/172 | -23.4% | -$199.13 | 3 | 154 | too early |
| 6 | fade_move | 113 | 32/113 | -46.5% | -$262.72 | 4 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 840 | 423/840 | -2.9% | -$122.54 | 4 | 215 | yardstick |

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
| 2026-11-09 | -$2.12 | -$2.15 | +$11.80 | -$112.41 | -$57.65 | -$79.27 | +$26.11 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Will BK Häcken FF win on 2026-11-10? -> No at 0.933 ($5.00)
- 2026-11-09 safe_no_week: Will the price of XRP be above $1.30 on November 16? -> No at 0.980 ($5.00)
- 2026-11-09 follow_move: Will the 2026 League of Legends World Championship peak concurrent viewers be at least 6 million? -> No at 0.730 ($5.00)
- 2026-11-09 sports_underdog: Will Plymouth Parkway FC vs. Berkhamsted FC end in a draw? -> Yes at 0.229 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Los Angeles be between 82-83°F on November 11? -> No at 0.671 ($5.00)
- 2026-11-09 fade_move: Will Palantir Technologies Inc. (PLTR) hit (LOW) $153 Week of November 9 2026? -> Yes at 0.194 ($5.00)
- 2026-11-09 coin_flip: XRP Up or Down - November 10, 10:40AM-10:45AM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: Will the price of Bitcoin be between $70,000 and $72,000 on November 10? -> No at 0.972 ($4.86)
- 2026-11-09 safe_no_week: Will the highest temperature in San Francisco be between 74-75°F on November 11? -> No at 0.971 ($5.00)
- 2026-11-09 follow_move: Will the price of Ethereum be above $2,200 on November 15? -> No at 0.734 ($5.00)
- 2026-11-09 sports_underdog: Spread: CD Tecnico Universitario (-2.5) -> CD Tecnico Universitario at 0.259 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Mexico City be 24°C on November 11? -> No at 0.699 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (4 with a problem).
Latest problem: 2 position(s) still open more than 3 days after their market ended
