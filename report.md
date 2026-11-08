# Polymarket strategy lab (pretend money)

Updated 2026-11-08 14:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 480 | 452/480 | -0.1% | -$2.57 | 3 | 247 | too early |
| 2 | safe_no_week | 50 | 48/50 | -0.3% | -$0.81 | 3 | 300 | too early |
| 3 | sports_underdog | 545 | 120/545 | -16.1% | -$435.65 | 3 | 95 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 123 | too early |
| 5 | weather_forecast | 78 | 37/78 | -25.8% | -$99.73 | 2 | 182 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 133 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 405 | 205/405 | -1.5% | -$30.11 | 3 | 323 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | sports_underdog | follow_move | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$9.15 | -$2.08 | -$193.55 |  | +$7.54 | +$1.40 | -$90.47 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Exact Score: Sporting CP B 0 - 0 CD Tondela? -> No at 0.933 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Sao Paulo be 19°C on November 10? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Spread: FK Shakhtar Donetsk (-1.5) -> FK Shakhtar Donetsk at 0.331 ($5.00)
- 2026-11-08 follow_move: Will CoreWeave say "Revenue" 20+ times during earnings call? -> Yes at 0.699 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Shanghai be 16°C on November 10? -> No at 0.642 ($5.00)
- 2026-11-08 fade_move: Will CoreWeave say "Revenue" 20+ times during earnings call? -> No at 0.359 ($5.00)
- 2026-11-08 coin_flip: Solana Up or Down - November 9, 7:55AM-8:00AM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Exact Score: NJ/NY Gotham FC 0 - 0 Seattle Reign FC? -> No at 0.962 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Buenos Aires be 25°C on November 10? -> No at 0.971 ($5.00)
- 2026-11-08 sports_underdog: Will FC Midtjylland win on 2026-11-08? -> No at 0.280 ($5.00)
- 2026-11-08 follow_move: Will IShowSpeed win Best IRL Streamer at the 2026 Streamer Awards? -> Yes at 0.827 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Seattle be between 58-59°F on November 10? -> No at 0.730 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
