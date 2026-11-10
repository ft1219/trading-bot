# Polymarket strategy lab (pretend money)

Updated 2026-11-10 19:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 158 | 96/158 | +1.1% | +$8.57 | 5 | 164 | too early |
| 2 | safe_no_week | 251 | 238/251 | -1.2% | -$15.24 | 5 | 340 | too early |
| 3 | sure_thing | 1088 | 1005/1088 | -1.4% | -$78.57 | 5 | 146 | too early |
| 4 | sports_underdog | 891 | 201/891 | -16.0% | -$708.39 | 5 | 62 | too early |
| 5 | weather_forecast | 241 | 118/241 | -26.7% | -$316.13 | 4 | 160 | too early |
| 6 | fade_move | 178 | 52/178 | -29.6% | -$262.97 | 5 | 176 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1132 | 552/1132 | -6.6% | -$374.79 | 5 | 227 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | safe_no_week | sure_thing | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | +$54.23 | +$8.69 | -$15.80 | -$21.45 | -$98.25 | -$12.52 | -$252.64 |
| 2026-11-09 | +$11.06 | -$5.28 | +$1.64 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | +$16.06 | -$19.92 | -$52.70 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | +$2.49 | +$0.90 | -$25.83 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | -$75.28 | +$0.37 | +$14.11 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> No at 0.738 ($5.00)
- 2026-11-10 safe_no_week: Will Airbnb, Inc. (ABNB) hit (HIGH) $202 Week of November 9 2026? -> No at 0.981 ($5.00)
- 2026-11-10 sure_thing: Will Spartak Myjava win on 2026-11-11? -> No at 0.962 ($5.00)
- 2026-11-10 sports_underdog: BNP Paribas Nordic Open: Lorenzo Musetti vs Toby Samuel -> Toby Samuel at 0.229 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in San Francisco be between 56-57°F on November 11? -> No at 0.626 ($5.00)
- 2026-11-10 fade_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> Yes at 0.329 ($5.00)
- 2026-11-10 coin_flip: Eastern Kentucky Colonels vs. Georgia Tech Yellow Jackets: O/U 159.5 -> Over at 0.661 ($5.00)
- 2026-11-10 follow_move: XRP Up or Down on November 11? -> Up at 0.756 ($5.00)
- 2026-11-10 safe_no_week: Will the price of Solana be between $60 and $70 on November 17? -> No at 0.986 ($5.00)
- 2026-11-10 sure_thing: Ethereum above 2,030 on November 10, 3PM ET? -> Yes at 0.963 ($5.00)
- 2026-11-10 sports_underdog: Will CD Leganés win on 2026-10-28? -> No at 0.167 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Denver be between 68-69°F on November 12? -> No at 0.492 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
