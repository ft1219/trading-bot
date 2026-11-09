# Polymarket strategy lab (pretend money)

Updated 2026-11-09 13:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 839 | 773/839 | -2.2% | -$93.58 | 4 | 123 | too early |
| 2 | safe_no_week | 131 | 122/131 | -3.2% | -$21.03 | 4 | 308 | too early |
| 3 | follow_move | 80 | 42/80 | -15.1% | -$60.38 | 4 | 166 | too early |
| 4 | sports_underdog | 746 | 165/746 | -16.3% | -$603.42 | 4 | 24 | too early |
| 5 | weather_forecast | 151 | 74/151 | -25.6% | -$191.35 | 3 | 164 | too early |
| 6 | fade_move | 95 | 30/95 | -40.7% | -$193.46 | 4 | 178 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 793 | 394/793 | -4.6% | -$182.88 | 4 | 206 | yardstick |

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
| 2026-11-09 | -$29.16 | -$2.38 | -$3.66 | -$98.47 | -$49.88 | -$10.00 | -$34.24 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: BNB Up or Down - November 9, 8AM ET -> Down at 0.916 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Houston be between 72-73°F on November 11? -> No at 0.952 ($5.00)
- 2026-11-09 follow_move: Gold (XAUUSD) Up or Down on November 9? -> Up at 0.845 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: InterActive Philippines vs CyberHero (BO3) - DreamLeague Division 2 Group B -> InterActive Philippines at 0.229 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Toronto be 13°C on November 11? -> No at 0.818 ($4.30)
- 2026-11-09 fade_move: Microsoft (MSFT) Up or Down on November 9? -> Down at 0.114 ($5.00)
- 2026-11-09 coin_flip: Ethereum Up or Down - November 10, 8:00AM-8:05AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Ethereum above 2,110 on November 9, 9AM ET? -> Yes at 0.925 ($5.00)
- 2026-11-09 safe_no_week: Will Tesla (TSLA) close at $340-$345 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will Tesla, Inc. (TSLA) hit (HIGH) $382.50 Week of November 9 2026? -> Yes at 0.440 ($5.00)
- 2026-11-09 sports_underdog: Counter-Strike: HAVU vs BOJONG (BO3) - Elisa Open Suomi Group Stage -> BOJONG at 0.232 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Helsinki be 2°C on November 10? -> No at 0.808 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
