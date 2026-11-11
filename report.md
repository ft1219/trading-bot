# Polymarket strategy lab (pretend money)

Updated 2026-11-11 15:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 192 | 118/192 | +1.8% | +$17.00 | 6 | 173 | too early |
| 2 | sure_thing | 1284 | 1192/1284 | -0.5% | -$31.85 | 6 | 134 | too early |
| 3 | safe_no_week | 311 | 293/311 | -1.8% | -$27.45 | 6 | 355 | too early |
| 4 | sports_underdog | 998 | 229/998 | -14.5% | -$720.20 | 6 | 44 | too early |
| 5 | fade_move | 214 | 64/214 | -23.7% | -$253.37 | 6 | 191 | too early |
| 6 | weather_forecast | 293 | 146/293 | -25.6% | -$369.77 | 5 | 169 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1348 | 667/1348 | -5.2% | -$351.80 | 6 | 251 | yardstick |

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
| 2026-11-11 | +$6.82 | +$46.84 | -$0.88 | -$95.20 | -$4.05 | -$50.72 | -$15.05 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: S&P 500 (SPY) closes above $755 on November 11? -> Yes at 0.600 ($5.00)
- 2026-11-11 sure_thing: Bitcoin above 74,000 on November 11, 11AM ET? -> No at 0.944 ($5.00)
- 2026-11-11 safe_no_week: Will Tesla (TSLA) close above $370 on November 12? -> Yes at 0.973 ($5.00)
- 2026-11-11 sports_underdog: Sopo: Irene Burillo Escorihuela vs Julia Grabher -> Irene Burillo Escorihuela at 0.270 ($5.00)
- 2026-11-11 fade_move: Will Apple (AAPL) close above $350 on November 11? -> No at 0.162 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Qingdao be 16°C on November 13? -> No at 0.671 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Hyperliquid Up or Down - November 11, 11:20PM-11:25PM ET -> Down at 0.527 ($5.00)
- 2026-11-11 follow_move: Will "Ghost Soldier" Opening Weekend Box Office be between 4m and 5m? -> Yes at 0.482 ($5.00)
- 2026-11-11 sure_thing: Exact Score: Ghana 1 - 0 Somalia? -> No at 0.904 ($5.00)
- 2026-11-11 safe_no_week: Will Google (GOOGL) close above $300 on November 12? -> No at 0.952 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: OLDBOYS- vs RoundsGG (BO1) - ESEA Advanced Europe Regular Season -> RoundsGG at 0.242 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
