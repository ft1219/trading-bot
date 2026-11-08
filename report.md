# Polymarket strategy lab (pretend money)

Updated 2026-11-08 21:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 663 | 614/663 | -1.8% | -$59.57 | 3 | 141 | too early |
| 2 | safe_no_week | 85 | 79/85 | -3.5% | -$14.99 | 3 | 287 | too early |
| 3 | sports_underdog | 645 | 144/645 | -14.9% | -$478.71 | 3 | 75 | too early |
| 4 | follow_move | 75 | 38/75 | -23.8% | -$89.00 | 3 | 118 | too early |
| 5 | weather_forecast | 110 | 53/110 | -25.8% | -$140.10 | 2 | 159 | too early |
| 6 | fade_move | 91 | 30/91 | -38.1% | -$173.46 | 3 | 131 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 598 | 298/598 | -3.8% | -$113.89 | 3 | 210 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | sports_underdog | follow_move | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | -$47.86 | -$16.26 | -$236.60 | -$16.21 | -$32.83 | -$6.21 | -$174.25 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: East Texas A&M Lions vs. SMU Mustangs (W) -> SMU Mustangs at 0.943 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Ethereum be above $1,900 on November 15? -> Yes at 0.972 ($5.00)
- 2026-11-08 sports_underdog: Will Antigua GFC win on 2026-11-08? -> No at 0.351 ($5.00)
- 2026-11-08 follow_move: Will the price of Solana be above $90 on November 14? -> No at 0.577 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Madrid be 17°C on November 9? -> No at 0.684 ($5.00)
- 2026-11-08 fade_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> No at 0.552 ($5.00)
- 2026-11-08 coin_flip: Hyperliquid Up or Down - November 9, 6:15AM-6:30AM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Bucky Irving: 2+ Touchdowns -> No at 0.924 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Atlanta be between 68-69°F on November 10? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Spread: CD Tolima (-1.5) -> CD Tolima at 0.187 ($5.00)
- 2026-11-08 follow_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> Yes at 0.512 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Milan be 6°C on November 9? -> Yes at 0.163 ($4.55)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
