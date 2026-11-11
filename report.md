# Polymarket strategy lab (pretend money)

Updated 2026-11-11 16:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 193 | 119/193 | +1.9% | +$18.28 | 6 | 173 | too early |
| 2 | sure_thing | 1285 | 1193/1285 | -0.5% | -$31.71 | 6 | 141 | too early |
| 3 | safe_no_week | 312 | 293/312 | -2.1% | -$32.45 | 6 | 355 | too early |
| 4 | sports_underdog | 1000 | 229/1000 | -14.7% | -$730.20 | 6 | 48 | too early |
| 5 | fade_move | 215 | 64/215 | -24.0% | -$258.37 | 6 | 191 | too early |
| 6 | weather_forecast | 293 | 146/293 | -25.6% | -$369.77 | 5 | 170 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1355 | 671/1355 | -5.2% | -$348.88 | 6 | 252 | yardstick |

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
| 2026-11-11 | +$8.10 | +$46.99 | -$5.88 | -$105.20 | -$9.05 | -$50.72 | -$12.13 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will "Victorian Psycho" score at least 75 on the Rotten Tomatoes Tomatometer? -> No at 0.642 ($5.00)
- 2026-11-11 sure_thing: Exact Score: Madagascar 0 - 0 Guinea-Bissau? -> No at 0.924 ($5.00)
- 2026-11-11 safe_no_week: Will Target Q3 comparable sales growth be between 1% and 3%? -> No at 0.976 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: ex-Zero Tenacity vs Spirit Academy (BO3) - NODWIN Clutch Series Group Stage -> Spirit Academy at 0.310 ($5.00)
- 2026-11-11 fade_move: WTI Crude Oil (WTI) Up or Down on November 11? -> Down at 0.139 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Moscow be 4°C on November 13? -> No at 0.616 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Spread: Rotherham United FC (-5.5) -> Rotherham United FC at 0.557 ($5.00)
- 2026-11-11 follow_move: S&P 500 (SPY) closes above $755 on November 11? -> Yes at 0.600 ($5.00)
- 2026-11-11 sure_thing: Will the US national average gas price be less than $3.9200 on November 12? -> Yes at 0.971 ($5.00)
- 2026-11-11 safe_no_week: Will Tesla (TSLA) close above $370 on November 12? -> Yes at 0.973 ($5.00)
- 2026-11-11 sports_underdog: Lima: Tristan Boyer vs Ryo Tabata -> Ryo Tabata at 0.177 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 38 position(s) still open more than 3 days after their market ended
