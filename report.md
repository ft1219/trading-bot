# Polymarket strategy lab (pretend money)

Updated 2026-11-08 20:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 640 | 597/640 | -1.1% | -$34.66 | 3 | 149 | too early |
| 2 | safe_no_week | 80 | 74/80 | -4.0% | -$16.14 | 3 | 289 | too early |
| 3 | sports_underdog | 631 | 139/631 | -16.0% | -$500.58 | 3 | 73 | too early |
| 4 | follow_move | 74 | 38/74 | -22.7% | -$84.00 | 3 | 119 | too early |
| 5 | weather_forecast | 107 | 53/107 | -23.7% | -$125.44 | 2 | 160 | too early |
| 6 | fade_move | 90 | 29/90 | -40.8% | -$183.57 | 3 | 132 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 569 | 282/569 | -5.7% | -$161.30 | 3 | 223 | yardstick |

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
| 2026-11-08 | -$22.95 | -$17.41 | -$258.48 | -$11.21 | -$18.16 | -$16.33 | -$221.65 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Spread: Kristiansund BK (-2.5) -> Vålerenga Fotball at 0.931 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Ethereum be between $2,500 and $2,600 on November 15? -> No at 0.986 ($5.00)
- 2026-11-08 sports_underdog: Spread: Sportivo Trinidense (-1.5) -> Sportivo Trinidense at 0.290 ($5.00)
- 2026-11-08 follow_move: Will the price of Solana be above $90 on November 14? -> No at 0.577 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Tokyo be 10°C on November 10? -> No at 0.684 ($5.00)
- 2026-11-08 fade_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> No at 0.552 ($5.00)
- 2026-11-08 coin_flip: XRP Up or Down - November 9, 2:25PM-2:30PM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Exact Score: Alianza FC 0 - 0 Llaneros FC? -> No at 0.914 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Munich be 7°C on November 10? -> No at 0.980 ($5.00)
- 2026-11-08 sports_underdog: Spread: CD Unión La Calera (-1.5) -> CD Unión La Calera at 0.244 ($5.00)
- 2026-11-08 follow_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> Yes at 0.512 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Istanbul be 12°C on November 9? -> Yes at 0.125 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
