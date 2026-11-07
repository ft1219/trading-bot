# Polymarket strategy lab (pretend money)

Updated 2026-11-07 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 134 | 127/134 | +0.8% | +$5.10 | 2 | 209 | too early |
| 2 | sports_underdog | 186 | 40/186 | -15.3% | -$140.74 | 2 | 78 | too early |
| 3 | follow_move | 44 | 20/44 | -36.7% | -$80.65 | 2 | 97 | too early |
| 4 | fade_move | 59 | 18/59 | -38.2% | -$112.78 | 2 | 100 | too early |
| 5 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 227 | too early |
| 6 | weather_forecast | 3 | 1/3 | -53.7% | -$8.06 | 1 | 148 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 73 | 36/73 | +1.0% | +$3.67 | 2 | 271 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | safe_no_week | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$9.01 | -$141.58 | -$5.37 | -$18.43 | +$0.25 | -$8.06 | -$3.76 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 | +$0.37 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Exact Score: Chesterfield FC 0 - 0 Yeovil Town FC? -> No at 0.967 ($5.00)
- 2026-11-07 sports_underdog: Will Borneo Samarinda vs. PSM Makassar end in a draw? -> Yes at 0.259 ($5.00)
- 2026-11-07 follow_move: Will Christopher Luxon be the next Prime Minister of New Zealand after the 2026 elections? -> Yes at 0.787 ($5.00)
- 2026-11-07 fade_move: Will Christopher Luxon be the next Prime Minister of New Zealand after the 2026 elections? -> No at 0.258 ($5.00)
- 2026-11-07 safe_no_week: Will the lowest temperature in Shenzhen be 20°C on November 9? -> No at 0.971 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Manila be 31°C on November 9? -> Yes at 0.112 ($4.74)
- 2026-11-07 coin_flip: OFI Crete vs. Atromitos Athinon: Draw at halftime? -> Yes at 0.452 ($5.00)
- 2026-11-07 sure_thing: Charleston Battery vs. Hartford Athletic: O/U 0.5 -> Over at 0.962 ($5.00)
- 2026-11-07 sports_underdog: Spread: Hwaseong FC (-1.5) -> Hwaseong FC at 0.300 ($5.00)
- 2026-11-07 follow_move: Will UK GDP growth in Q3 2026 be between 0.6% and 0.7%? -> Yes at 0.575 ($5.00)
- 2026-11-07 fade_move: Will the price of Ethereum be above $2,100 on November 12? -> No at 0.158 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Tel Aviv be 20°C on November 9? -> No at 0.981 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
