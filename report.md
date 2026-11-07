# Polymarket strategy lab (pretend money)

Updated 2026-11-07 20:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 26 | 26/26 | +4.2% | +$5.44 | 2 | 273 | too early |
| 2 | sure_thing | 336 | 318/336 | +0.3% | +$5.83 | 2 | 175 | too early |
| 3 | sports_underdog | 346 | 75/346 | -15.0% | -$257.98 | 2 | 82 | too early |
| 4 | follow_move | 59 | 31/59 | -23.0% | -$67.78 | 2 | 104 | too early |
| 5 | fade_move | 74 | 21/74 | -45.7% | -$169.18 | 2 | 113 | too early |
| 6 | weather_forecast | 34 | 9/34 | -59.5% | -$101.16 | 1 | 163 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 204 | 110/204 | +6.5% | +$66.24 | 2 | 308 | yardstick |

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
| 2026-11-07 | +$5.08 | -$8.28 | -$258.82 | +$7.49 | -$74.83 | -$101.16 | +$58.81 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will the highest temperature in Kuala Lumpur be 34°C on November 9? -> No at 0.971 ($5.00)
- 2026-11-07 sure_thing: Ratchaburi FC vs. Buriram United: O/U 5.5 -> Under at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Spread: Libertad Asuncion (-1.5) -> Libertad Asuncion at 0.218 ($5.00)
- 2026-11-07 follow_move: Solana Up or Down on November 8? -> Down at 0.646 ($5.00)
- 2026-11-07 fade_move: XRP Up or Down on November 8? -> Up at 0.407 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Miami be between 74-75°F on November 9? -> No at 0.750 ($5.00)
- 2026-11-07 coin_flip: FK Haugesund vs. Odds BK: Odds BK O/U 1.5 -> Over at 0.442 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Moscow be 4°C on November 9? -> No at 0.924 ($5.00)
- 2026-11-07 sure_thing: Will FK Akron Tolyatti win on 2026-11-08? -> No at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Kentucky vs. Tennessee -> Kentucky at 0.357 ($5.00)
- 2026-11-07 follow_move: XRP Up or Down on November 8? -> Down at 0.650 ($5.00)
- 2026-11-07 fade_move: Solana Up or Down on November 8? -> Up at 0.402 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
