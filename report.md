# Polymarket strategy lab (pretend money)

Updated 2026-11-09 15:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 849 | 783/849 | -2.0% | -$86.47 | 4 | 130 | too early |
| 2 | safe_no_week | 136 | 127/136 | -2.9% | -$20.03 | 4 | 311 | too early |
| 3 | follow_move | 82 | 44/82 | -13.7% | -$56.04 | 4 | 165 | too early |
| 4 | sports_underdog | 752 | 167/752 | -16.2% | -$607.37 | 4 | 30 | too early |
| 5 | weather_forecast | 156 | 77/156 | -25.0% | -$193.08 | 3 | 166 | too early |
| 6 | fade_move | 97 | 30/97 | -41.9% | -$203.46 | 4 | 177 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 809 | 403/809 | -4.1% | -$166.81 | 4 | 214 | yardstick |

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
| 2026-11-09 | -$22.05 | -$1.39 | +$0.69 | -$102.41 | -$51.61 | -$20.00 | -$18.17 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Bitcoin above 75,600 on November 9, 11AM ET? -> No at 0.906 ($5.00)
- 2026-11-09 safe_no_week: Will Tesla (TSLA) finish week of November 9 above $345? -> Yes at 0.933 ($5.00)
- 2026-11-09 follow_move: Rocket Lab (RKLB) Up or Down on November 9? -> Up at 0.659 ($5.00)
- 2026-11-09 sports_underdog: Spread: FC Botoşani (-1.5) -> FC Botoşani at 0.259 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Istanbul be 18°C on November 11? -> No at 0.691 ($5.00)
- 2026-11-09 fade_move: Rocket Lab (RKLB) Up or Down on November 9? -> Down at 0.413 ($5.00)
- 2026-11-09 coin_flip: Ethereum Up or Down - November 10, 6:15AM-6:30AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: EWY (EWY) Up or Down on November 9? -> Up at 0.933 ($5.00)
- 2026-11-09 safe_no_week: Will UKMTO publish 16 or more notices between November 9-November 15? -> No at 0.970 ($5.00)
- 2026-11-09 follow_move: Gold (XAUUSD) Up or Down on November 9? -> Up at 0.845 ($5.00)
- 2026-11-09 sports_underdog: Will Kristiansund BK win on 2026-11-07? -> Yes at 0.361 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Austin be between 68-69°F on November 10? -> No at 0.720 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
