# Polymarket strategy lab (pretend money)

Updated 2026-11-09 09:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 819 | 756/819 | -2.1% | -$84.16 | 4 | 109 | too early |
| 2 | safe_no_week | 125 | 116/125 | -3.5% | -$22.02 | 4 | 300 | too early |
| 3 | follow_move | 79 | 41/79 | -15.6% | -$61.73 | 4 | 155 | too early |
| 4 | sports_underdog | 744 | 164/744 | -16.2% | -$600.98 | 4 | 13 | too early |
| 5 | weather_forecast | 150 | 74/150 | -25.1% | -$186.35 | 3 | 160 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 168 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 755 | 381/755 | -3.1% | -$116.10 | 4 | 197 | yardstick |

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
| 2026-11-09 | -$19.75 | -$3.37 | -$5.00 | -$96.03 | -$44.88 |  | +$32.54 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: BNB Up or Down - November 9, 4AM ET -> Down at 0.906 ($5.00)
- 2026-11-09 safe_no_week: Will S&P 500 (SPY) hit (HIGH) $770 Week of November 9 2026? -> No at 0.933 ($5.00)
- 2026-11-09 follow_move: Will Micron (MU) finish week of November 9 above $720? -> No at 0.731 ($5.00)
- 2026-11-09 sports_underdog: Mobile Legends Bang Bang: The World vs Rakuzan (BO3) - BetBoom Rise of Legends Group A -> The World at 0.331 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Chongqing be 11°C on November 11? -> No at 0.759 ($5.00)
- 2026-11-09 fade_move: Will Micron (MU) finish week of November 9 above $720? -> Yes at 0.339 ($5.00)
- 2026-11-09 coin_flip: ZCash Up or Down - November 9, 2:30PM-2:45PM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Bitcoin Up or Down - November 9, 4AM ET -> Down at 0.943 ($5.00)
- 2026-11-09 safe_no_week: Will NVIDIA (NVDA) hit (HIGH) $208 Week of November 9 2026? -> No at 0.981 ($5.00)
- 2026-11-09 follow_move: WTI Crude Oil (WTI) Up or Down on November 9? -> Down at 0.836 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: Froglings vs Team Synapse (BO3) - DreamLeague Division 2 Group A -> Team Synapse at 0.352 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Paris be 16°C on November 11? -> No at 0.701 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
