# Polymarket strategy lab (pretend money)

Updated 2026-11-06 21:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 50 | 49/50 | +4.0% | +$9.97 | 1 | 182 | too early |
| 2 | sports_underdog | 75 | 16/75 | -21.8% | -$81.03 | 1 | 80 | too early |
| 3 | follow_move | 33 | 17/33 | -27.5% | -$45.28 | 1 | 100 | too early |
| 4 | fade_move | 42 | 11/42 | -47.5% | -$99.66 | 1 | 107 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 193 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 127 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 26 | 13/26 | -8.8% | -$11.47 | 1 | 206 | yardstick |

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

| Day | sure_thing | sports_underdog | follow_move | fade_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-06 | +$9.97 | -$81.03 | -$45.28 | -$99.66 | +$0.12 | -$11.47 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Spread: Columbus Crew (-2.5) -> Chicago Fire FC at 0.952 ($5.00)
- 2026-11-06 sports_underdog: UNCG Spartans vs. Elon Phoenix -> UNCG Spartans at 0.229 ($5.00)
- 2026-11-06 follow_move: Will 170-189 ships transit the Bab el-Mandeb Strait between November 2-November 8? -> No at 0.840 ($5.00)
- 2026-11-06 fade_move: Will 170-189 ships transit the Bab el-Mandeb Strait between November 2-November 8? -> Yes at 0.200 ($5.00)
- 2026-11-06 safe_no_week: Will the lowest temperature in Hong Kong be 24°C on November 8? -> No at 0.962 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Helsinki be -1°C on November 7? -> No at 0.740 ($5.00)
- 2026-11-06 coin_flip: Timberwolves vs. Pelicans -> Pelicans at 0.422 ($5.00)
- 2026-11-06 sure_thing: Spread: Garuda Yaksa (-2.5) -> Persijap Jepara at 0.943 ($5.00)
- 2026-11-06 sports_underdog: Northern Iowa Panthers vs. South Dakota State Jackrabbits (W) -> Northern Iowa Panthers at 0.167 ($5.00)
- 2026-11-06 follow_move: Will the price of Ethereum be between $2,200 and $2,300 on November 10? -> Yes at 0.417 ($5.00)
- 2026-11-06 fade_move: Will the price of Ethereum be between $2,200 and $2,300 on November 10? -> No at 0.676 ($5.00)
- 2026-11-06 safe_no_week: Will the lowest temperature in Seoul (Incheon) be 5°C on November 8? -> No at 0.952 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 29 (0 with a problem).
