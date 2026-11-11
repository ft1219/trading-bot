# Polymarket strategy lab (pretend money)

Updated 2026-11-11 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 185 | 113/185 | +1.0% | +$8.86 | 6 | 150 | too early |
| 2 | sure_thing | 1240 | 1151/1240 | -0.5% | -$30.33 | 6 | 111 | too early |
| 3 | safe_no_week | 290 | 273/290 | -1.9% | -$27.81 | 6 | 322 | too early |
| 4 | sports_underdog | 983 | 225/983 | -14.7% | -$719.72 | 6 | 15 | too early |
| 5 | fade_move | 205 | 62/205 | -23.5% | -$240.86 | 6 | 167 | too early |
| 6 | weather_forecast | 273 | 136/273 | -25.8% | -$346.35 | 5 | 145 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1277 | 624/1277 | -6.4% | -$407.01 | 6 | 218 | yardstick |

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
| 2026-11-11 | -$1.33 | +$48.37 | -$1.24 | -$94.72 | +$8.47 | -$27.30 | -$70.26 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> No at 0.223 ($5.00)
- 2026-11-11 sure_thing: Magic vs. Jazz: O/U 245.5 -> Under at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in London be 6°C on November 13? -> No at 0.952 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: MOUZ vs G2 (BO3) - BLAST Rivals Group B -> G2 at 0.239 ($5.00)
- 2026-11-11 fade_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> Yes at 0.818 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Taipei be 31°C on November 13? -> No at 0.622 ($5.00)
- 2026-11-11 coin_flip: Thunder vs. Trail Blazers: O/U 226.5 -> Over at 0.532 ($5.00)
- 2026-11-11 follow_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> Yes at 0.351 ($5.00)
- 2026-11-11 sure_thing: Ethereum above 2,050 on November 11, 2AM ET? -> Yes at 0.906 ($5.00)
- 2026-11-11 safe_no_week: Will the lowest temperature in Paris be 7°C on November 12? -> No at 0.929 ($5.00)
- 2026-11-11 sports_underdog: LoL: Ground Zero Gaming vs Frank Esports (BO5) - LCP Promotion Playoffs -> Frank Esports at 0.216 ($5.00)
- 2026-11-11 fade_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> No at 0.691 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
