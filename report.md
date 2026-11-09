# Polymarket strategy lab (pretend money)

Updated 2026-11-09 16:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 856 | 789/856 | -2.1% | -$89.76 | 4 | 131 | too early |
| 2 | safe_no_week | 150 | 140/150 | -3.0% | -$22.30 | 4 | 308 | too early |
| 3 | follow_move | 83 | 44/83 | -14.7% | -$61.04 | 4 | 171 | too early |
| 4 | sports_underdog | 752 | 167/752 | -16.2% | -$607.37 | 4 | 44 | too early |
| 5 | weather_forecast | 172 | 87/172 | -23.4% | -$199.13 | 3 | 150 | too early |
| 6 | fade_move | 98 | 31/98 | -39.7% | -$194.53 | 4 | 186 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 820 | 410/820 | -3.8% | -$156.02 | 4 | 219 | yardstick |

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
| 2026-11-09 | -$25.34 | -$3.66 | -$4.31 | -$102.41 | -$57.65 | -$11.08 | -$7.38 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Manta FC leading at halftime? -> No at 0.904 ($5.00)
- 2026-11-09 safe_no_week: Will Meta (META) close above $610 on November 10? -> Yes at 0.971 ($5.00)
- 2026-11-09 follow_move: Will SpaceX (SPCX) hit (HIGH) $152.50 Week of November 9 2026? -> Yes at 0.339 ($5.00)
- 2026-11-09 sports_underdog: Will CE Sabadell FC vs. Real Sociedad de Fútbol B end in a draw? -> Yes at 0.270 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Istanbul be 18°C on November 11? -> No at 0.691 ($5.00)
- 2026-11-09 fade_move: Will Tesla (TSLA) close at >$380 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.580 ($5.00)
- 2026-11-09 coin_flip: XRP Up or Down - November 10, 6:00AM-6:15AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Will Solana reach $90 on November 9? -> No at 0.916 ($5.00)
- 2026-11-09 safe_no_week: Will 40 or more ships transit the Strait of Hormuz between November 9-November 15? -> No at 0.950 ($5.00)
- 2026-11-09 follow_move: Will the price of Solana be between $90 and $100 on November 13? -> No at 0.773 ($5.00)
- 2026-11-09 sports_underdog: Will Calcio Foggia vs. Barletta Calcio end in a draw? -> Yes at 0.321 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Austin be between 68-69°F on November 10? -> No at 0.720 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (2 with a problem).
Latest problem: 2 position(s) still open more than 3 days after their market ended
