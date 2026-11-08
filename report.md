# Polymarket strategy lab (pretend money)

Updated 2026-11-08 22:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 690 | 638/690 | -1.9% | -$67.01 | 3 | 122 | too early |
| 2 | safe_no_week | 87 | 81/87 | -3.4% | -$14.77 | 3 | 286 | too early |
| 3 | sports_underdog | 657 | 144/657 | -16.5% | -$538.71 | 3 | 71 | too early |
| 4 | follow_move | 76 | 39/76 | -23.1% | -$87.70 | 3 | 121 | too early |
| 5 | weather_forecast | 112 | 55/112 | -24.4% | -$134.75 | 2 | 158 | too early |
| 6 | fade_move | 92 | 30/92 | -38.8% | -$178.46 | 3 | 133 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 615 | 305/615 | -4.4% | -$134.93 | 3 | 201 | yardstick |

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
| 2026-11-08 | -$55.30 | -$16.03 | -$296.60 | -$14.91 | -$27.48 | -$11.21 | -$195.29 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Spread: AZ Picerno (-1.5) -> SSC Bari at 0.924 ($5.00)
- 2026-11-08 safe_no_week: Will Amazon (AMZN) close at $270-$275 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.942 ($5.00)
- 2026-11-08 sports_underdog: Lightning vs. Jets: O/U 4.5 -> Under at 0.229 ($5.00)
- 2026-11-08 follow_move: Bitcoin Up or Down on November 9? -> Down at 0.802 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Dallas be between 76-77°F on November 10? -> No at 0.711 ($5.00)
- 2026-11-08 fade_move: XRP Up or Down on November 9? -> Up at 0.150 ($5.00)
- 2026-11-08 coin_flip: Ethereum Up or Down - November 8, 8:25PM-8:30PM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Exact Score: CD Tecnico Universitario 0 - 0 Manta FC? -> No at 0.933 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Ethereum be above $1,900 on November 15? -> Yes at 0.972 ($5.00)
- 2026-11-08 sports_underdog: Norfolk State Spartans vs. William & Mary Tribe -> Norfolk State Spartans at 0.177 ($5.00)
- 2026-11-08 follow_move: Will the price of Bitcoin be above $72,000 on November 13? -> No at 0.284 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Madrid be 17°C on November 9? -> No at 0.684 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
