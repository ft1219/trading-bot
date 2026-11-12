# Polymarket strategy lab (pretend money)

Updated 2026-11-12 10:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 227 | 139/227 | +0.9% | +$10.70 | 7 | 166 | too early |
| 2 | sure_thing | 1423 | 1322/1423 | -0.4% | -$30.84 | 7 | 204 | too early |
| 3 | safe_no_week | 378 | 354/378 | -2.4% | -$44.45 | 7 | 356 | too early |
| 4 | sports_underdog | 1121 | 256/1121 | -14.9% | -$832.49 | 7 | 29 | too early |
| 5 | fade_move | 257 | 77/257 | -20.6% | -$264.58 | 7 | 175 | too early |
| 6 | weather_forecast | 349 | 179/349 | -21.9% | -$376.72 | 6 | 153 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1533 | 759/1533 | -5.2% | -$395.70 | 7 | 280 | yardstick |

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
| 2026-11-12 | -$9.17 | -$11.35 | +$0.90 | -$34.08 | +$34.81 | +$20.24 | -$29.08 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> Yes at 0.522 ($5.00)
- 2026-11-12 sure_thing: Will Meta (META) close above $650 on November 12? -> No at 0.962 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Chicago be between 48-49°F on November 14? -> No at 0.933 ($5.00)
- 2026-11-12 sports_underdog: Games Total: O/U 2.5 -> Over at 0.305 ($5.00)
- 2026-11-12 fade_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> No at 0.512 ($5.00)
- 2026-11-12 weather_forecast: Will the highest temperature in Ankara be 18°C or higher on November 14? -> No at 0.680 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Bitcoin Up or Down - November 12, 1:15PM-1:20PM ET -> Down at 0.517 ($5.00)
- 2026-11-12 follow_move: Will NYC Mayor post 20-39 posts from November 6 to November 13, 2026? -> Yes at 0.701 ($5.00)
- 2026-11-12 sure_thing: Croatia to win the second half? -> No at 0.904 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Dallas be between 66-67°F on November 14? -> No at 0.981 ($5.00)
- 2026-11-12 sports_underdog: Monastir: Marvin Moeller vs Aziz Ouakaa -> Aziz Ouakaa at 0.280 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 35 (35 with a problem).
Latest problem: 35 position(s) still open more than 3 days after their market ended
