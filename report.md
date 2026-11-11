# Polymarket strategy lab (pretend money)

Updated 2026-11-11 23:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 222 | 137/222 | +1.8% | +$19.88 | 6 | 161 | too early |
| 2 | sure_thing | 1353 | 1259/1353 | -0.3% | -$19.49 | 6 | 151 | too early |
| 3 | safe_no_week | 352 | 329/352 | -2.6% | -$45.36 | 6 | 337 | too early |
| 4 | sports_underdog | 1042 | 235/1042 | -15.4% | -$798.41 | 6 | 63 | too early |
| 5 | fade_move | 249 | 73/249 | -24.1% | -$299.39 | 6 | 173 | too early |
| 6 | weather_forecast | 322 | 162/322 | -25.1% | -$396.96 | 5 | 150 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1427 | 708/1427 | -5.2% | -$366.62 | 6 | 258 | yardstick |

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
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: BNB Up or Down on November 12? -> Down at 0.792 ($5.00)
- 2026-11-11 sure_thing: Exact Score: Cerro Largo FC 0 - 0 CA Progreso? -> No at 0.933 ($5.00)
- 2026-11-11 safe_no_week: Will the price of XRP be between $0.80 and $0.90 on November 18? -> No at 0.981 ($5.00)
- 2026-11-11 sports_underdog: Stephen F. Austin Lumberjacks vs. Abilene Christian Wildcats -> Abilene Christian Wildcats at 0.310 ($5.00)
- 2026-11-11 fade_move: BNB Up or Down on November 12? -> Up at 0.284 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Ankara be 9°C or higher on November 13? -> No at 0.635 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Hyperliquid Up or Down - November 12, 5:00AM-5:05AM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Solana Up or Down on November 12? -> Down at 0.734 ($5.00)
- 2026-11-11 sure_thing: Spread: Athletic Club (-1.5) -> São Bernardo FC at 0.933 ($5.00)
- 2026-11-11 safe_no_week: Will "Victorian Psycho" Opening Weekend Box Office be less than 2.5m? -> Yes at 0.943 ($5.00)
- 2026-11-11 sports_underdog: Magic vs. Jazz: O/U 223.5 -> Over at 0.341 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 35 (35 with a problem).
Latest problem: weather: Open-Meteo failed for KORD, no more forecasts fetched this run: https://ensemble-api.open-meteo.com/v1/ensemble?latitude=41.96017&longitude=-87.93161&models=ecmwf_ifs025%2Cgfs_seamless&timezo
