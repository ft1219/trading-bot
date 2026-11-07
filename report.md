# Polymarket strategy lab (pretend money)

Updated 2026-11-07 23:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 33 | 32/33 | +0.8% | +$1.27 | 2 | 269 | too early |
| 2 | sure_thing | 381 | 357/381 | -0.6% | -$11.72 | 2 | 162 | too early |
| 3 | sports_underdog | 384 | 87/384 | -12.7% | -$242.10 | 2 | 75 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 106 | too early |
| 5 | fade_move | 75 | 22/75 | -44.6% | -$167.24 | 2 | 115 | too early |
| 6 | weather_forecast | 47 | 17/47 | -45.6% | -$107.27 | 1 | 154 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 251 | 133/251 | +4.8% | +$60.36 | 2 | 293 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | +$0.90 | -$25.83 | -$242.94 | +$2.49 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will the price of Bitcoin be above $68,000 on November 14? -> Yes at 0.981 ($5.00)
- 2026-11-07 sure_thing: Exact Score: SK Slavia Praha 1 - 0 SK Artis Brno? -> No at 0.933 ($5.00)
- 2026-11-07 sports_underdog: Spread: CF Cruz Azul (-1.5) -> CF Cruz Azul at 0.270 ($5.00)
- 2026-11-07 follow_move: Will Rocket Lab (RKLB) beat quarterly earnings? -> No at 0.818 ($5.00)
- 2026-11-07 fade_move: Will Rocket Lab (RKLB) beat quarterly earnings? -> Yes at 0.249 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Jeddah be 25°C on November 9? -> No at 0.655 ($5.00)
- 2026-11-07 coin_flip: Bitcoin Up or Down - November 8, 7:25AM-7:30AM ET -> Up at 0.527 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Jeddah be 30°C on November 9? -> No at 0.962 ($5.00)
- 2026-11-07 sure_thing: Spread: FC Seoul (-2.5) -> Ulsan HD FC at 0.904 ($5.00)
- 2026-11-07 sports_underdog: Spread: CR Brasil (-2.5) -> CR Brasil at 0.270 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 8? -> Down at 0.753 ($5.00)
- 2026-11-07 fade_move: Dogecoin Up or Down on November 8? -> Up at 0.325 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 37 (0 with a problem).
