# Polymarket strategy lab (pretend money)

Updated 2026-11-10 16:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 235 | 223/235 | -1.1% | -$13.21 | 5 | 342 | too early |
| 2 | sure_thing | 1062 | 981/1062 | -1.4% | -$74.85 | 5 | 148 | too early |
| 3 | follow_move | 139 | 85/139 | -1.6% | -$11.44 | 5 | 169 | too early |
| 4 | sports_underdog | 883 | 199/883 | -15.9% | -$699.84 | 5 | 52 | too early |
| 5 | fade_move | 158 | 47/158 | -26.1% | -$206.28 | 5 | 180 | too early |
| 6 | weather_forecast | 238 | 116/238 | -27.0% | -$315.99 | 4 | 159 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1112 | 544/1112 | -6.3% | -$350.62 | 5 | 215 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | follow_move | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | +$10.72 | -$12.08 | +$34.22 | -$12.89 | +$44.18 | -$98.10 | -$228.47 |
| 2026-11-09 | -$5.28 | +$1.64 | +$11.06 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | -$19.92 | -$52.70 | +$16.06 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$0.90 | -$25.83 | +$2.49 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | +$0.37 | +$14.11 | -$75.28 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 safe_no_week: Will the lowest temperature in Shanghai be 17°C on November 12? -> No at 0.971 ($5.00)
- 2026-11-10 sure_thing: Will the US national average gas price be less than $3.9600 on November 11? -> Yes at 0.971 ($4.86)
- 2026-11-10 follow_move: Will the price of XRP be between $1.00 and $1.10 on November 11? -> Yes at 0.805 ($5.00)
- 2026-11-10 sports_underdog: Monastir: Gabriel Debru vs Mae Malige -> Mae Malige at 0.229 ($5.00)
- 2026-11-10 fade_move: Will Palantir (PLTR) close at >$170 on the final day of trading of the week of Nov 9 – Nov 13? -> Yes at 0.359 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Houston be between 64-65°F on November 11? -> No at 0.701 ($5.00)
- 2026-11-10 coin_flip: BNB Up or Down - November 10, 6:15PM-6:30PM ET -> Down at 0.527 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Qingdao be 16°C on November 12? -> No at 0.942 ($5.00)
- 2026-11-10 sure_thing: Micron (MU) Up or Down on November 10? -> Down at 0.971 ($5.00)
- 2026-11-10 follow_move: Will Elon Musk post 260-279 tweets from November 6 to November 13, 2026? -> Yes at 0.239 ($5.00)
- 2026-11-10 sports_underdog: Monastir: Nicolas Tepmahc vs Lorenzo Giustino -> Nicolas Tepmahc at 0.218 ($5.00)
- 2026-11-10 fade_move: Will Elon Musk post 260-279 tweets from November 6 to November 13, 2026? -> No at 0.808 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
