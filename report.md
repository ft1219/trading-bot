# Polymarket strategy lab (pretend money)

Updated 2026-11-12 08:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 226 | 138/226 | +0.6% | +$7.01 | 7 | 167 | too early |
| 2 | sure_thing | 1414 | 1315/1414 | -0.3% | -$23.47 | 7 | 191 | too early |
| 3 | safe_no_week | 374 | 351/374 | -2.1% | -$39.87 | 7 | 339 | too early |
| 4 | sports_underdog | 1115 | 251/1115 | -15.6% | -$866.31 | 7 | 26 | too early |
| 5 | fade_move | 256 | 77/256 | -20.3% | -$259.58 | 7 | 176 | too early |
| 6 | weather_forecast | 345 | 177/345 | -23.6% | -$401.00 | 6 | 148 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1519 | 753/1519 | -5.1% | -$382.75 | 7 | 270 | yardstick |

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
| 2026-11-12 | -$12.86 | -$3.98 | +$5.48 | -$67.90 | +$39.81 | -$4.04 | -$16.13 |
| 2026-11-11 | +$9.69 | +$59.21 | -$18.78 | -$173.41 | -$50.06 | -$77.92 | -$29.87 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-12 follow_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> Yes at 0.522 ($5.00)
- 2026-11-12 sure_thing: Dota 2: CyberHero vs Team Allied (BO3) - Asgard Championship Group B -> CyberHero at 0.924 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Lucknow be 28°C on November 14? -> No at 0.984 ($5.00)
- 2026-11-12 sports_underdog: Hannover 96 vs. TSV Havelse: O/U 2.5 -> Under at 0.267 ($5.00)
- 2026-11-12 fade_move: Will "The Gospel of Christmas" be the top global Netflix movie this week? -> No at 0.512 ($5.00)
- 2026-11-12 weather_forecast: Will the highest temperature in Singapore be 32°C on November 14? -> No at 0.779 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-12 coin_flip: Bitcoin Up or Down - November 12, 4:45AM-4:50AM ET -> Down at 0.517 ($5.00)
- 2026-11-12 follow_move: Will NYC Mayor post 20-39 posts from November 6 to November 13, 2026? -> Yes at 0.701 ($5.00)
- 2026-11-12 sure_thing: Will Bonaire win on 2026-11-12? -> No at 0.962 ($5.00)
- 2026-11-12 safe_no_week: Will the highest temperature in Istanbul be 23°C on November 14? -> No at 0.983 ($5.00)
- 2026-11-12 sports_underdog: Will RB Leipzig win on 2026-11-12? -> No at 0.156 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
