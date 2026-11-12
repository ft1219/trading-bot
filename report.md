# Polymarket strategy lab (pretend money)

Updated 2026-11-12 04:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 224 | 137/224 | +0.9% | +$9.88 | 7 | 165 | too early |
| 2 | sure_thing | 1387 | 1291/1387 | -0.2% | -$15.77 | 7 | 171 | too early |
| 3 | safe_no_week | 361 | 338/361 | -2.4% | -$43.05 | 7 | 335 | too early |
| 4 | sports_underdog | 1086 | 244/1086 | -16.0% | -$863.71 | 7 | 45 | too early |
| 5 | fade_move | 254 | 76/254 | -20.8% | -$263.82 | 7 | 174 | too early |
| 6 | weather_forecast | 330 | 167/330 | -24.7% | -$400.64 | 6 | 142 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1474 | 732/1474 | -5.1% | -$371.81 | 7 | 267 | yardstick |

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
| 2026-11-12 | -$10.00 | +$3.72 | +$2.31 | -$65.30 | +$35.57 | -$3.68 | -$5.19 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will MrBeast's next video get between 35 and 40 million views on day 1? -> Yes at 0.259 ($5.00)
- 2026-11-12 sure_thing: Spread: SV Meppen 1912 (-1.5) -> Arminia Bielefeld at 0.962 ($5.00)
- 2026-11-12 safe_no_week: Will Mark Rothko's “Untitled” sell for at least $6.5m at auction? -> No at 0.962 ($5.00)
- 2026-11-12 sports_underdog: Counter-Strike: FUT Esports vs MOUZ (BO3) - BLAST Rivals Group B -> FUT Esports at 0.177 ($5.00)
- 2026-11-12 fade_move: Will MrBeast's next video get between 35 and 40 million views on day 1? -> No at 0.798 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Ankara be 9°C or higher on November 13? -> No at 0.635 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Bitcoin Up or Down - November 12, 10:45PM-10:50PM ET -> Down at 0.517 ($5.00)
- 2026-11-12 follow_move: Will "Reminders of Him" be the #2 US Netflix movie this week? -> Yes at 0.442 ($5.00)
- 2026-11-12 sure_thing: Spread: AA Ponte Preta (-1.5) -> Operário Ferroviário EC at 0.952 ($5.00)
- 2026-11-12 safe_no_week: Will "Allen" be the #2 global Netflix movie this week? -> No at 0.924 ($5.00)
- 2026-11-12 sports_underdog: Games Total: O/U 4.5 -> Over at 0.202 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
