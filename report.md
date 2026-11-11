# Polymarket strategy lab (pretend money)

Updated 2026-11-11 07:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 186 | 113/186 | +0.4% | +$3.86 | 6 | 149 | too early |
| 2 | sure_thing | 1246 | 1157/1246 | -0.5% | -$28.38 | 6 | 108 | too early |
| 3 | safe_no_week | 298 | 280/298 | -2.1% | -$30.84 | 6 | 317 | too early |
| 4 | sports_underdog | 986 | 226/986 | -14.6% | -$714.65 | 6 | 16 | too early |
| 5 | fade_move | 207 | 63/207 | -23.4% | -$242.41 | 6 | 165 | too early |
| 6 | weather_forecast | 281 | 142/281 | -24.7% | -$341.36 | 5 | 141 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1283 | 628/1283 | -6.2% | -$399.18 | 6 | 220 | yardstick |

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
| 2026-11-11 | -$6.33 | +$50.31 | -$4.26 | -$89.65 | +$6.91 | -$22.32 | -$62.43 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> No at 0.223 ($5.00)
- 2026-11-11 sure_thing: BNB Up or Down - November 11, 2AM ET -> Up at 0.916 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Busan be 17°C on November 13? -> No at 0.924 ($5.00)
- 2026-11-11 sports_underdog: Orleans: Jurij Rodionov vs Pedro Martinez -> Pedro Martinez at 0.259 ($5.00)
- 2026-11-11 fade_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> Yes at 0.818 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Tokyo be 11°C on November 13? -> No at 0.798 ($5.00)
- 2026-11-11 coin_flip: BNB Up or Down - November 12, 12:20AM-12:25AM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> Yes at 0.351 ($5.00)
- 2026-11-11 sure_thing: Bitcoin Up or Down - November 11, 2AM ET -> Up at 0.906 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Guangzhou be 21°C on November 13? -> No at 0.981 ($5.00)
- 2026-11-11 sports_underdog: Dota 2: PlayTime vs Team Synapse (BO3) - DreamLeague Division 2 Group A -> Team Synapse at 0.249 ($5.00)
- 2026-11-11 fade_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> No at 0.691 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 1.005 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
