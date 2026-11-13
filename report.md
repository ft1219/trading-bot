# Polymarket strategy lab (pretend money)

Updated 2026-11-13 10:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 258 | 161/258 | +2.1% | +$26.89 | 8 | 135 | too early |
| 2 | sure_thing | 1638 | 1522/1638 | -0.5% | -$42.27 | 8 | 8 | too early |
| 3 | safe_no_week | 463 | 433/463 | -2.5% | -$57.94 | 8 | 287 | too early |
| 4 | fade_move | 289 | 88/289 | -12.9% | -$187.02 | 8 | 143 | too early |
| 5 | sports_underdog | 1164 | 266/1164 | -14.9% | -$861.96 | 8 | 4 | too early |
| 6 | weather_forecast | 417 | 209/417 | -23.7% | -$487.52 | 7 | 89 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1722 | 856/1722 | -4.4% | -$381.19 | 8 | 115 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | fade_move | sports_underdog | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-13 | +$1.88 | -$15.37 | -$9.77 | -$33.06 | +$3.98 | -$39.33 | +$45.67 |
| 2026-11-12 | +$5.13 | -$7.41 | -$2.81 | +$145.43 | -$67.52 | -$51.23 | -$60.24 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$50.06 | -$173.41 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$1.13 | +$61.94 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$67.00 | -$181.99 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$16.21 | -$262.85 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$72.89 | -$242.94 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | -$94.35 | +$0.84 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> Yes at 0.522 ($5.00)
- 2026-11-12 sure_thing: Canisius Golden Griffins vs. Brown Bears -> Brown Bears at 0.904 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Hong Kong be 24°C on November 14? -> No at 0.924 ($5.00)
- 2026-11-12 fade_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> No at 0.512 ($5.00)
- 2026-11-12 sports_underdog: BNP Paribas Nordic Open: Alex Michelsen vs Alejandro Tabilo -> Alejandro Tabilo at 0.239 ($5.00)
- 2026-11-12 weather_forecast: Will the highest temperature in New York City be between 44-45°F on November 14? -> Yes at 0.125 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Solana Up or Down - November 13, 8AM ET -> Up at 0.527 ($5.00)
- 2026-11-12 follow_move: Will NYC Mayor post 20-39 posts from November 6 to November 13, 2026? -> Yes at 0.701 ($5.00)
- 2026-11-12 sure_thing: Ethereum above 2,040 on November 12, 8AM ET? -> No at 0.972 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in New York City be between 42-43°F on November 14? -> No at 0.960 ($5.00)
- 2026-11-12 fade_move: Will NYC Mayor post 20-39 posts from November 6 to November 13, 2026? -> No at 0.373 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: events: 7 slice reads failed, Gamma seems down: https://gamma-api.polymarket.com/events?active=true&closed=false&limit=100&offset=0&end_date_min=2026-11-14T22%3A47%3A22Z&end_date_max=2026-11-15T04%3A4
