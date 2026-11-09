# Polymarket strategy lab (pretend money)

Updated 2026-11-09 02:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 756 | 699/756 | -1.9% | -$72.98 | 4 | 110 | too early |
| 2 | safe_no_week | 99 | 92/99 | -3.6% | -$17.72 | 4 | 290 | too early |
| 3 | follow_move | 78 | 41/78 | -14.6% | -$56.73 | 3 | 137 | too early |
| 4 | sports_underdog | 702 | 157/702 | -15.0% | -$524.91 | 4 | 50 | too early |
| 5 | weather_forecast | 127 | 65/127 | -21.7% | -$136.50 | 3 | 152 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 151 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 688 | 346/688 | -2.9% | -$98.67 | 4 | 184 | yardstick |

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
| 2026-11-09 | -$8.56 | +$0.93 |  | -$19.96 | +$4.97 |  | +$49.97 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Exact Score: Chelmsford City 0 - 0 Ebbsfleet United FC? -> No at 0.962 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Moscow be 3°C on November 10? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will Silver (XAGUSD) hit (LOW) $50 Week of November 9 2026? -> No at 0.718 ($5.00)
- 2026-11-09 sports_underdog: Rainbow Six Siege: Fluxo W7M vs EDward Gaming (BO3) - BLAST R6 Major Osaka Phase 2 -> EDward Gaming at 0.187 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Chongqing be 11°C on November 10? -> No at 0.671 ($5.00)
- 2026-11-09 fade_move: Dogecoin Up or Down on November 9? -> Up at 0.356 ($5.00)
- 2026-11-09 coin_flip: Solana Up or Down - November 9, 6:30PM-6:45PM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Spread: ASC Oțelul Galați (-1.5) -> FC Botoşani at 0.904 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Houston be between 70-71°F on November 10? -> No at 0.924 ($5.00)
- 2026-11-09 follow_move: Dow Jones (DJIA) Up or Down on November 9? -> Up at 0.826 ($5.00)
- 2026-11-09 sports_underdog: USC Trojans vs. Wichita State Shockers -> Wichita State Shockers at 0.310 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Houston be between 60-61°F on November 10? -> No at 0.681 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 37 (0 with a problem).
