# Polymarket strategy lab (pretend money)

Updated 2026-11-11 19:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 208 | 130/208 | +4.0% | +$41.60 | 6 | 169 | too early |
| 2 | sure_thing | 1311 | 1219/1311 | -0.3% | -$22.80 | 6 | 153 | too early |
| 3 | safe_no_week | 335 | 315/335 | -2.0% | -$33.41 | 6 | 348 | too early |
| 4 | sports_underdog | 1008 | 229/1008 | -15.4% | -$770.20 | 6 | 57 | too early |
| 5 | weather_forecast | 310 | 154/310 | -26.0% | -$395.99 | 5 | 159 | too early |
| 6 | fade_move | 230 | 68/230 | -26.8% | -$307.48 | 6 | 186 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1393 | 689/1393 | -5.4% | -$375.09 | 6 | 252 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-11 | +$31.41 | +$55.90 | -$6.83 | -$145.20 | -$76.95 | -$58.16 | -$38.34 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | -$101.16 | +$1.13 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will hate that i made you love me (Ariana Grande) be nominated for Best Pop Solo Performance at the 69th Annual GRAMMY Awards? -> No at 0.622 ($5.00)
- 2026-11-11 sure_thing: Exact Score: Barbados 0 - 0 Guadeloupe? -> No at 0.952 ($5.00)
- 2026-11-11 safe_no_week: Will "Allen" be the top global Netflix movie this week? -> No at 0.971 ($5.00)
- 2026-11-11 sports_underdog: Spread: Londrina EC (-1.5) -> Londrina EC at 0.300 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Tel Aviv be 12°C on November 13? -> No at 0.876 ($5.00)
- 2026-11-11 fade_move: Will Microsoft (MSFT) finish week of November 9 above $540? -> Yes at 0.114 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Spread: Wisconsin (-2.5) -> Wisconsin at 0.720 ($5.00)
- 2026-11-11 follow_move: Will the price of Ethereum be between $2,100 and $2,200 on November 17? -> Yes at 0.315 ($5.00)
- 2026-11-11 sure_thing: Will Chambéry Savoie Football win on 2026-11-12? -> No at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Hong Kong be 28°C on November 13? -> No at 0.952 ($5.00)
- 2026-11-11 sports_underdog: Will Londrina EC vs. Clube Náutico Capibaribe end in a draw? -> Yes at 0.259 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 38 position(s) still open more than 3 days after their market ended
