# Polymarket strategy lab (pretend money)

Updated 2026-11-10 16:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1062 | 981/1062 | -1.4% | -$74.85 | 5 | 144 | too early |
| 2 | safe_no_week | 221 | 209/221 | -1.5% | -$16.40 | 5 | 352 | too early |
| 3 | follow_move | 137 | 84/137 | -1.7% | -$11.64 | 5 | 167 | too early |
| 4 | sports_underdog | 882 | 199/882 | -15.8% | -$694.84 | 5 | 45 | too early |
| 5 | weather_forecast | 223 | 108/223 | -27.5% | -$303.12 | 4 | 170 | too early |
| 6 | fade_move | 156 | 45/156 | -34.0% | -$264.61 | 5 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1106 | 542/1106 | -6.1% | -$338.55 | 5 | 213 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | follow_move | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | -$12.08 | +$7.53 | +$34.02 | -$7.89 | -$85.24 | -$14.16 | -$216.40 |
| 2026-11-09 | +$1.64 | -$5.28 | +$11.06 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Will Rumble (RUM) beat quarterly earnings? -> No at 0.914 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Munich be 14°C on November 12? -> No at 0.933 ($5.00)
- 2026-11-10 follow_move: Will AECOM (ACM) beat quarterly earnings? -> No at 0.229 ($5.00)
- 2026-11-10 sports_underdog: Will SD Amorebieta win on 2026-10-28? -> Yes at 0.297 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Munich be 12°C on November 12? -> No at 0.592 ($5.00)
- 2026-11-10 fade_move: Will AECOM (ACM) beat quarterly earnings? -> Yes at 0.837 ($5.00)
- 2026-11-10 coin_flip: Dogecoin Up or Down - November 11, 10:30AM-10:45AM ET -> Up at 0.527 ($5.00)
- 2026-11-10 sure_thing: S&P 500 (SPX) Up or Down on November 10? -> Down at 0.913 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Toronto be 9°C on November 12? -> No at 0.971 ($5.00)
- 2026-11-10 follow_move: Will Tyson Foods (TSN) beat quarterly earnings? -> No at 0.351 ($5.00)
- 2026-11-10 sports_underdog: Spread: UD Logroñés (-1.5) -> UD Logroñés at 0.247 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Toronto be 6°C on November 12? -> No at 0.711 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
