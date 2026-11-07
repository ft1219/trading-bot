# Polymarket strategy lab (pretend money)

Updated 2026-11-07 22:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 29 | 28/29 | +0.5% | +$0.77 | 2 | 271 | too early |
| 2 | sure_thing | 369 | 347/369 | -0.2% | -$4.60 | 2 | 158 | too early |
| 3 | sports_underdog | 368 | 82/368 | -12.9% | -$234.90 | 2 | 75 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 106 | too early |
| 5 | fade_move | 75 | 22/75 | -44.6% | -$167.24 | 2 | 115 | too early |
| 6 | weather_forecast | 37 | 11/37 | -53.8% | -$99.59 | 1 | 162 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 235 | 124/235 | +4.6% | +$53.36 | 2 | 293 | yardstick |

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
| 2026-11-07 | +$0.41 | -$18.71 | -$235.74 | +$2.49 | -$72.89 | -$99.59 | +$45.93 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will Trump's approval rating be at least 40.0 on November 13, 2026? -> No at 0.971 ($5.00)
- 2026-11-07 sure_thing: CF Universidad de Chile vs. CD Cobresal: O/U 6.5 -> Under at 0.962 ($5.00)
- 2026-11-07 sports_underdog: Southern Indiana Screaming Eagles vs. Evansville Aces -> Southern Indiana Screaming Eagles at 0.267 ($5.00)
- 2026-11-07 follow_move: Will Rocket Lab (RKLB) beat quarterly earnings? -> No at 0.818 ($5.00)
- 2026-11-07 fade_move: Will Rocket Lab (RKLB) beat quarterly earnings? -> Yes at 0.249 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Chongqing be 12°C on November 9? -> No at 0.723 ($5.00)
- 2026-11-07 coin_flip: Fredrikstad FK vs. SK Brann: SK Brann O/U 1.5 -> Under at 0.542 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Kuala Lumpur be 34°C on November 9? -> No at 0.971 ($5.00)
- 2026-11-07 sure_thing: Spread: NK Brinje Grosuplje (-2.5) -> Aluminij Kidricevo at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Spread: Indiana State (-3.5) -> Indiana State at 0.306 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 8? -> Down at 0.753 ($5.00)
- 2026-11-07 fade_move: Dogecoin Up or Down on November 8? -> Up at 0.325 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
