# Polymarket strategy lab (pretend money)

Updated 2026-11-08 22:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 702 | 649/702 | -2.0% | -$69.07 | 3 | 118 | too early |
| 2 | safe_no_week | 91 | 84/91 | -4.2% | -$19.19 | 3 | 286 | too early |
| 3 | follow_move | 78 | 41/78 | -14.6% | -$56.73 | 3 | 120 | too early |
| 4 | sports_underdog | 664 | 146/664 | -16.1% | -$531.12 | 3 | 72 | too early |
| 5 | weather_forecast | 116 | 58/116 | -23.2% | -$132.81 | 2 | 155 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 135 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 629 | 310/629 | -5.0% | -$157.68 | 3 | 195 | yardstick |

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
| 2026-11-08 | -$57.35 | -$20.46 | +$16.06 | -$289.02 | -$25.54 | -$16.21 | -$218.04 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Ethereum Up or Down on November 9? -> Down at 0.925 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Karachi be 33°C on November 10? -> No at 0.944 ($5.00)
- 2026-11-08 follow_move: Will the price of Solana be above $80 on November 13? -> No at 0.253 ($5.00)
- 2026-11-08 sports_underdog: Spread: Alianza FC (-1.5) -> Alianza FC at 0.198 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Jeddah be 33°C on November 10? -> No at 0.730 ($5.00)
- 2026-11-08 fade_move: Ethereum Up or Down on November 9? -> Up at 0.096 ($5.00)
- 2026-11-08 coin_flip: Nuggets vs. Rockets -> Nuggets at 0.280 ($5.00)
- 2026-11-08 sure_thing: Exact Score: AZ Picerno 0 - 0 SSC Bari? -> No at 0.914 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Solana be above $75 on November 15? -> Yes at 0.944 ($5.00)
- 2026-11-08 follow_move: Bitcoin Up or Down on November 9? -> Down at 0.802 ($5.00)
- 2026-11-08 sports_underdog: Rainbow Six Siege: Sharper Esport vs LOS (BO1) - BLAST R6 Major Osaka Phase 2 -> Sharper Esport at 0.331 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Dallas be between 76-77°F on November 10? -> No at 0.711 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
