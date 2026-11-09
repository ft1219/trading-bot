# Polymarket strategy lab (pretend money)

Updated 2026-11-09 16:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 850 | 783/850 | -2.2% | -$91.47 | 4 | 133 | too early |
| 2 | safe_no_week | 136 | 127/136 | -2.9% | -$20.03 | 4 | 318 | too early |
| 3 | follow_move | 83 | 44/83 | -14.7% | -$61.04 | 4 | 165 | too early |
| 4 | sports_underdog | 752 | 167/752 | -16.2% | -$607.37 | 4 | 36 | too early |
| 5 | weather_forecast | 156 | 77/156 | -25.0% | -$193.08 | 3 | 166 | too early |
| 6 | fade_move | 98 | 31/98 | -39.7% | -$194.53 | 4 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 816 | 408/816 | -3.7% | -$149.97 | 4 | 215 | yardstick |

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
| 2026-11-09 | -$27.05 | -$1.39 | -$4.31 | -$102.41 | -$51.61 | -$11.08 | -$1.33 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: XRP Up or Down - November 9, 11:00AM-11:15AM ET -> Down at 0.953 ($5.00)
- 2026-11-09 safe_no_week: Will Rocket Lab USA, Inc. (RKLB) hit (LOW) $42 Week of November 9 2026? -> No at 0.971 ($5.00)
- 2026-11-09 follow_move: Will Robinhood Markets, Inc. (HOOD) hit (HIGH) $92.50 Week of November 9 2026? -> Yes at 0.342 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: PuckChamp vs Zero Tenacity (BO3) - DreamLeague Division 2 Group B -> PuckChamp at 0.331 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Istanbul be 18°C on November 11? -> No at 0.691 ($5.00)
- 2026-11-09 fade_move: Will Rocket Lab USA, Inc. (RKLB) hit (LOW) $46 Week of November 9 2026? -> Yes at 0.188 ($5.00)
- 2026-11-09 coin_flip: Bitcoin Up or Down - November 9, 7:25PM-7:30PM ET -> Down at 0.517 ($5.00)
- 2026-11-09 sure_thing: Ethereum above 2,160 on November 9, 12PM ET? -> No at 0.953 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Singapore be 33°C on November 11? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Rocket Lab (RKLB) Up or Down on November 9? -> Up at 0.659 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: Yakult Brothers vs Inner Circle (BO3) - DreamLeague Division 2 Group B -> Yakult Brothers at 0.208 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Austin be between 68-69°F on November 10? -> No at 0.720 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (1 with a problem).
Latest problem: 2 position(s) still open more than 3 days after their market ended
