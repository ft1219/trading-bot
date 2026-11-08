# Polymarket strategy lab (pretend money)

Updated 2026-11-08 20:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 652 | 606/652 | -1.4% | -$46.94 | 3 | 144 | too early |
| 2 | safe_no_week | 80 | 74/80 | -4.0% | -$16.14 | 3 | 292 | too early |
| 3 | sports_underdog | 638 | 141/638 | -15.7% | -$499.14 | 3 | 74 | too early |
| 4 | follow_move | 74 | 38/74 | -22.7% | -$84.00 | 3 | 119 | too early |
| 5 | weather_forecast | 107 | 53/107 | -23.7% | -$125.44 | 2 | 162 | too early |
| 6 | fade_move | 90 | 29/90 | -40.8% | -$183.57 | 3 | 132 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 582 | 290/582 | -4.3% | -$124.52 | 3 | 218 | yardstick |

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
| 2026-11-08 | -$35.22 | -$17.41 | -$257.04 | -$11.21 | -$18.16 | -$16.33 | -$184.87 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Spread: Buccaneers (-7.5) -> Bears at 0.903 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Ethereum be above $1,900 on November 15? -> Yes at 0.972 ($5.00)
- 2026-11-08 sports_underdog: Will Barcelona SC vs. LDU Quito end in a draw? -> Yes at 0.310 ($5.00)
- 2026-11-08 follow_move: Will the price of Solana be above $90 on November 14? -> No at 0.577 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Madrid be 17°C on November 9? -> No at 0.684 ($5.00)
- 2026-11-08 fade_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> No at 0.552 ($5.00)
- 2026-11-08 coin_flip: Solana Up or Down - November 9, 1:15PM-1:30PM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Spread: Cancun FC (-1.5) -> Piratas Veracruz at 0.951 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Atlanta be between 68-69°F on November 10? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Will Deportivo La Guaira win on 2026-11-08? -> Yes at 0.328 ($5.00)
- 2026-11-08 follow_move: Will "Housewife - Tate McRae" be the #1 US song this week? -> Yes at 0.512 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Milan be 6°C on November 9? -> Yes at 0.163 ($4.55)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
