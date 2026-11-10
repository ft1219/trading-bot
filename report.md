# Polymarket strategy lab (pretend money)

Updated 2026-11-10 22:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 180 | 110/180 | +1.4% | +$12.84 | 5 | 143 | too early |
| 2 | sure_thing | 1149 | 1062/1149 | -1.4% | -$81.74 | 5 | 123 | too early |
| 3 | safe_no_week | 268 | 253/268 | -1.7% | -$22.33 | 5 | 333 | too early |
| 4 | sports_underdog | 918 | 211/918 | -13.9% | -$634.23 | 5 | 57 | too early |
| 5 | fade_move | 199 | 60/199 | -24.8% | -$246.88 | 5 | 156 | too early |
| 6 | weather_forecast | 252 | 125/252 | -26.0% | -$321.74 | 4 | 153 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1168 | 572/1168 | -6.0% | -$347.96 | 5 | 231 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | +$58.50 | -$18.97 | +$1.60 | +$52.72 | +$3.57 | -$103.85 | -$225.80 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Will Donald Trump post 200+ Truth Social posts from November 10 to November 17, 2026? -> No at 0.856 ($5.00)
- 2026-11-10 sure_thing: Exact Score: Malmo FF 0 - 1 Ajax Amsterdam? -> No at 0.943 ($5.00)
- 2026-11-10 safe_no_week: Will Getty Images (GETY) beat quarterly earnings? -> No at 0.972 ($5.00)
- 2026-11-10 sports_underdog: Avalanche vs. Maple Leafs: O/U 4.5 -> Under at 0.187 ($5.00)
- 2026-11-10 fade_move: Will Donald Trump post 200+ Truth Social posts from November 10 to November 17, 2026? -> Yes at 0.185 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Shanghai be 14°C on November 12? -> No at 0.661 ($5.00)
- 2026-11-10 coin_flip: Ethereum Up or Down - November 12, 3AM ET -> Down at 0.527 ($5.00)
- 2026-11-10 follow_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> No at 0.738 ($5.00)
- 2026-11-10 sure_thing: Spread: Clube Náutico Capibaribe (-1.5) -> Londrina EC at 0.953 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Seattle be between 54-55°F on November 12? -> No at 0.979 ($5.00)
- 2026-11-10 sports_underdog: Wild vs. Canadiens: O/U 4.5 -> Under at 0.229 ($5.00)
- 2026-11-10 fade_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> Yes at 0.329 ($5.00)

## Price gaps seen today

3 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
