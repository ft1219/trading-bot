# Polymarket strategy lab (pretend money)

Updated 2026-11-12 00:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 223 | 137/223 | +1.3% | +$14.88 | 7 | 161 | too early |
| 2 | sure_thing | 1363 | 1268/1363 | -0.3% | -$21.33 | 7 | 155 | too early |
| 3 | safe_no_week | 356 | 333/356 | -2.5% | -$44.48 | 7 | 335 | too early |
| 4 | sports_underdog | 1051 | 239/1051 | -14.8% | -$772.40 | 7 | 70 | too early |
| 5 | fade_move | 252 | 74/252 | -24.0% | -$302.75 | 7 | 171 | too early |
| 6 | weather_forecast | 328 | 166/328 | -24.6% | -$397.49 | 6 | 144 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1441 | 715/1441 | -5.2% | -$374.20 | 7 | 260 | yardstick |

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
| 2026-11-12 | -$5.00 | -$1.84 | +$0.88 | +$26.01 | -$3.36 | -$0.53 | -$7.58 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Dogecoin Up or Down on November 12? -> Down at 0.802 ($5.00)
- 2026-11-12 sure_thing: Overwatch: T1 vs MURASH GAMING (BO5) - OCS Asia Stage 3 Group A -> T1 at 0.962 ($5.00)
- 2026-11-12 safe_no_week: Will "Adin Ross's Team" win Nozempic 2? -> Yes at 0.982 ($5.00)
- 2026-11-12 sports_underdog: Matsuyama: Rei Sakamoto vs Kasidit Samrej -> Kasidit Samrej at 0.156 ($5.00)
- 2026-11-12 fade_move: Dogecoin Up or Down on November 12? -> Up at 0.284 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Ankara be 9°C or higher on November 13? -> No at 0.635 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Exeter City FC vs. Cheltenham Town FC: O/U 3.5 -> Under at 0.750 ($5.00)
- 2026-11-11 follow_move: BNB Up or Down on November 12? -> Down at 0.792 ($5.00)
- 2026-11-12 sure_thing: Spread: CSD Mixco (-1.5) -> Aurora FC at 0.914 ($5.00)
- 2026-11-12 safe_no_week: Will "Heartland" be the #2 US Netflix movie this week? -> No at 0.933 ($5.00)
- 2026-11-12 sports_underdog: Colorado Buffaloes vs. San Diego State Aztecs (W) -> San Diego State Aztecs at 0.361 ($1.81)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 35 (35 with a problem).
Latest problem: 38 position(s) still open more than 3 days after their market ended
