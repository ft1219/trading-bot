# Polymarket strategy lab (pretend money)

Updated 2026-11-09 12:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 834 | 769/834 | -2.2% | -$89.88 | 4 | 123 | too early |
| 2 | safe_no_week | 130 | 121/130 | -3.3% | -$21.32 | 4 | 308 | too early |
| 3 | follow_move | 80 | 42/80 | -15.1% | -$60.38 | 4 | 166 | too early |
| 4 | sports_underdog | 745 | 165/745 | -16.1% | -$598.42 | 4 | 20 | too early |
| 5 | weather_forecast | 151 | 74/151 | -25.6% | -$191.35 | 3 | 163 | too early |
| 6 | fade_move | 95 | 30/95 | -40.7% | -$193.46 | 4 | 178 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 784 | 391/784 | -4.3% | -$166.31 | 4 | 207 | yardstick |

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
| 2026-11-09 | -$25.47 | -$2.67 | -$3.66 | -$93.47 | -$49.88 | -$10.00 | -$17.67 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Microsoft (MSFT) Up or Down on November 9? -> Up at 0.962 ($5.00)
- 2026-11-09 safe_no_week: Will Tesla (TSLA) close at $340-$345 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Gold (XAUUSD) Up or Down on November 9? -> Up at 0.845 ($5.00)
- 2026-11-09 sports_underdog: Monastir: Bernardo Munk vs Aziz Dougaz -> Bernardo Munk at 0.156 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Helsinki be 2°C on November 10? -> No at 0.808 ($5.00)
- 2026-11-09 fade_move: Microsoft (MSFT) Up or Down on November 9? -> Down at 0.114 ($5.00)
- 2026-11-09 coin_flip: Ethereum Up or Down - November 10, 3:45AM-3:50AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Will Google (GOOGL) close above $285 on November 9? -> Yes at 0.933 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Beijing be 16°C on November 11? -> No at 0.981 ($5.00)
- 2026-11-09 follow_move: Will Tesla, Inc. (TSLA) hit (HIGH) $382.50 Week of November 9 2026? -> Yes at 0.440 ($5.00)
- 2026-11-09 sports_underdog: Monastir: Sandro Kopp vs Luka Mikrut -> Sandro Kopp at 0.300 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Tel Aviv be 14°C on November 11? -> Yes at 0.173 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
