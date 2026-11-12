# Polymarket strategy lab (pretend money)

Updated 2026-11-12 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 226 | 138/226 | +0.6% | +$7.01 | 7 | 165 | too early |
| 2 | sure_thing | 1413 | 1315/1413 | -0.3% | -$18.47 | 7 | 177 | too early |
| 3 | safe_no_week | 369 | 346/369 | -2.2% | -$41.03 | 7 | 337 | too early |
| 4 | sports_underdog | 1110 | 249/1110 | -15.8% | -$874.73 | 7 | 25 | too early |
| 5 | fade_move | 256 | 77/256 | -20.3% | -$259.58 | 7 | 174 | too early |
| 6 | weather_forecast | 337 | 173/337 | -23.6% | -$391.93 | 6 | 142 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1514 | 751/1514 | -5.0% | -$377.60 | 7 | 259 | yardstick |

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
| 2026-11-12 | -$12.86 | +$1.02 | +$4.33 | -$76.32 | +$39.81 | +$5.04 | -$10.97 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will "Black Doves: Season 2" be the #2 global Netflix show this week? -> Yes at 0.642 ($5.00)
- 2026-11-12 sure_thing: Czechia to win the second half? -> No at 0.914 ($5.00)
- 2026-11-12 safe_no_week: Will Khamenei post 0-4 posts from November 10 to November 17, 2026? -> Yes at 0.962 ($5.00)
- 2026-11-12 sports_underdog: Counter-Strike: Ducks vs DNK (BO3) - Exort Fiesta Closed Qualifier: Series #4 Group D -> DNK at 0.333 ($4.29)
- 2026-11-12 fade_move: Will "The Body: Season 1" be the #2 global Netflix show this week? -> Yes at 0.177 ($5.00)
- 2026-11-12 weather_forecast: Will the highest temperature in Wellington be 20°C on November 14? -> No at 0.808 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Will the price of Bitcoin be above $74,000 on November 12? -> No at 0.687 ($5.00)
- 2026-11-12 follow_move: Will "The Gospel of Christmas" be the top US Netflix movie this week? -> Yes at 0.711 ($5.00)
- 2026-11-12 sure_thing: Dota 2: PARIVISION vs DO KONCA (BO3) - 1win Essence Group A -> PARIVISION at 0.904 ($5.00)
- 2026-11-12 safe_no_week: Will Nvidia (NVDA) beat quarterly earnings? -> Yes at 0.971 ($5.00)
- 2026-11-12 sports_underdog: Counter-Strike: Spirit vs G2 (BO3) - BLAST Rivals Group B -> G2 at 0.280 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
