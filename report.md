# Polymarket strategy lab (pretend money)

Updated 2026-11-12 11:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 228 | 140/228 | +1.7% | +$19.49 | 7 | 165 | too early |
| 2 | sure_thing | 1426 | 1325/1426 | -0.4% | -$29.91 | 7 | 212 | too early |
| 3 | safe_no_week | 382 | 358/382 | -2.3% | -$43.59 | 7 | 362 | too early |
| 4 | sports_underdog | 1124 | 256/1124 | -15.2% | -$847.49 | 7 | 37 | too early |
| 5 | fade_move | 258 | 77/258 | -20.9% | -$269.58 | 7 | 174 | too early |
| 6 | weather_forecast | 354 | 180/354 | -22.6% | -$393.13 | 6 | 150 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1546 | 764/1546 | -5.4% | -$418.85 | 7 | 283 | yardstick |

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
| 2026-11-12 | -$0.39 | -$10.42 | +$1.77 | -$49.08 | +$29.81 | +$3.83 | -$52.23 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> Yes at 0.522 ($5.00)
- 2026-11-12 sure_thing: Ethereum Up or Down on November 12? -> Down at 0.916 ($5.00)
- 2026-11-12 safe_no_week: Will "Taken: Natalee Holloway: Season 1" be the top US Netflix show this week? -> Yes at 0.933 ($5.00)
- 2026-11-12 sports_underdog: Counter-Strike: INOX Division vs mixLVLT (BO3) - ESL Challenger League Europe Cup #12 Group B -> mixLVLT at 0.167 ($5.00)
- 2026-11-12 fade_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> No at 0.512 ($5.00)
- 2026-11-12 weather_forecast: Will the highest temperature in Los Angeles be between 72-73°F on November 14? -> No at 0.661 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Will Peru vs. Bolivia end in a draw? -> No at 0.779 ($5.00)
- 2026-11-12 follow_move: Will NYC Mayor post 20-39 posts from November 6 to November 13, 2026? -> Yes at 0.701 ($5.00)
- 2026-11-12 sure_thing: Eswatini leading at halftime? -> No at 0.904 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Sao Paulo be 30°C on November 14? -> No at 0.979 ($5.00)
- 2026-11-12 sports_underdog: Will Standard Liege win on 2026-11-12? -> Yes at 0.259 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 35 (35 with a problem).
Latest problem: 35 position(s) still open more than 3 days after their market ended
