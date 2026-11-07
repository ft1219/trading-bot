# Polymarket strategy lab (pretend money)

Updated 2026-11-07 13:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 169 | 161/169 | +1.3% | +$10.65 | 2 | 254 | too early |
| 2 | sports_underdog | 259 | 59/259 | -11.3% | -$145.13 | 2 | 81 | too early |
| 3 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 102 | too early |
| 4 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 110 | too early |
| 5 | weather_forecast | 10 | 2/10 | -68.6% | -$34.32 | 1 | 176 | too early |
| 6 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 268 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 100 | 55/100 | +8.2% | +$40.93 | 2 | 324 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$3.46 | -$145.97 | -$10.37 | -$23.43 | -$34.32 | +$0.25 | +$33.50 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Spread: Newport County AFC (-2.5) -> Walsall FC at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Spread: MSV Duisburg (-1.5) -> MSV Duisburg at 0.259 ($5.00)
- 2026-11-07 follow_move: Will NVIDIA (NVDA) close above $195 on November 9? -> No at 0.845 ($5.00)
- 2026-11-07 fade_move: Will Apple (AAPL) close above $335 on November 9? -> No at 0.156 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Los Angeles be between 84-85°F on November 9? -> No at 0.818 ($4.30)
- 2026-11-07 safe_no_week: Will the highest temperature in Taipei be 22°C on November 9? -> No at 0.981 ($5.00)
- 2026-11-07 coin_flip: Will LASK Linz win on 2026-11-07? -> Yes at 0.671 ($5.00)
- 2026-11-07 sure_thing: Exact Score: Paju Frontier FC 0 - 0 Chungnam Asan FC? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Will Luton Town FC win on 2026-11-07? -> No at 0.280 ($5.00)
- 2026-11-07 follow_move: Will the biggest earthquake on November 7, 2026 be 5.5 to 5.6? -> Yes at 0.711 ($5.00)
- 2026-11-07 fade_move: Will Microsoft (MSFT) close above $520 on November 9? -> No at 0.145 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Helsinki be 6°C on November 9? -> No at 0.632 ($5.00)

## Price gaps seen today

6 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 37 (0 with a problem).
