# Polymarket strategy lab (pretend money)

Updated 2026-11-10 06:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1019 | 942/1019 | -1.3% | -$67.43 | 5 | 102 | too early |
| 2 | follow_move | 136 | 83/136 | -2.1% | -$13.99 | 5 | 136 | too early |
| 3 | safe_no_week | 199 | 187/199 | -2.1% | -$20.93 | 5 | 308 | too early |
| 4 | sports_underdog | 847 | 192/847 | -15.0% | -$631.15 | 5 | 23 | too early |
| 5 | weather_forecast | 201 | 98/201 | -26.5% | -$263.26 | 4 | 140 | too early |
| 6 | fade_move | 155 | 45/155 | -33.5% | -$259.61 | 5 | 146 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1007 | 497/1007 | -5.4% | -$272.78 | 5 | 192 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | follow_move | safe_no_week | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | -$4.65 | +$31.68 | +$3.00 | +$55.80 | -$45.38 | -$9.16 | -$150.63 |
| 2026-11-09 | +$1.64 | +$11.06 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | +$16.06 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$2.49 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | -$75.28 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Feyenoord Rotterdam vs. VfL Wolfsburg: O/U 1.5 -> Over at 0.943 ($5.00)
- 2026-11-10 follow_move: Will Bitcoin dip to $72,000 November 9-15? -> No at 0.607 ($5.00)
- 2026-11-10 safe_no_week: Will Japan Q3 GDP growth (annualized) be between 1.6% and 2.4%? -> No at 0.939 ($5.00)
- 2026-11-10 sports_underdog: Counter-Strike: Brute vs ILLYRIANS (BO3) - NODWIN Clutch Series Group Stage -> ILLYRIANS at 0.357 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Ankara be 9°C on November 11? -> No at 0.632 ($5.00)
- 2026-11-10 fade_move: Will Bitcoin dip to $72,000 November 9-15? -> Yes at 0.437 ($5.00)
- 2026-11-10 coin_flip: Hyperliquid Up or Down - November 10, 4:55AM-5:00AM ET -> Up at 0.527 ($5.00)
- 2026-11-10 sure_thing: Bitcoin above 75,000 on November 10, 2AM ET? -> No at 0.953 ($5.00)
- 2026-11-10 follow_move: Will Kai Cenat finish his GTA marathon by November 11, 2:59 PM ET? -> Yes at 0.701 ($5.00)
- 2026-11-10 safe_no_week: Will gemini-4-argon-high be the best AI model on November 16, 2026? -> No at 0.985 ($5.00)
- 2026-11-10 sports_underdog: Counter-Strike: Bad Beavers vs Copenhagen Wolves (BO3) - United21 Group D -> Bad Beavers at 0.208 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Seattle be between 64-65°F on November 11? -> No at 0.582 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (22 with a problem).
Latest problem: 6 position(s) still open more than 3 days after their market ended
