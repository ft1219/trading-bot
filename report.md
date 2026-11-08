# Polymarket strategy lab (pretend money)

Updated 2026-11-08 00:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 36 | 35/36 | +0.9% | +$1.63 | 3 | 266 | too early |
| 2 | sure_thing | 398 | 374/398 | -0.4% | -$7.08 | 3 | 153 | too early |
| 3 | sports_underdog | 397 | 90/397 | -13.1% | -$257.71 | 3 | 70 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 108 | too early |
| 5 | weather_forecast | 50 | 19/50 | -42.5% | -$106.14 | 2 | 151 | too early |
| 6 | fade_move | 75 | 22/75 | -44.6% | -$167.24 | 2 | 117 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 263 | 139/263 | +3.8% | +$49.36 | 3 | 289 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$0.37 | +$4.64 | -$15.61 |  | +$1.13 |  | -$11.00 |
| 2026-11-07 | +$0.90 | -$25.83 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will the price of Bitcoin be above $68,000 on November 14? -> Yes at 0.981 ($5.00)
- 2026-11-08 sure_thing: Exact Score: FK Transinvest 0 - 0 FK Kauno Zalgiris? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Spread: Deportivo Toluca FC (-2.5) -> Deportivo Toluca FC at 0.198 ($5.00)
- 2026-11-08 follow_move: Will Apple (AAPL) hit (LOW) $324 Week of November 9 2026? -> No at 0.845 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Jeddah be 25°C on November 9? -> No at 0.655 ($5.00)
- 2026-11-08 fade_move: Will Constellation Energy say "Trump" during earnings call? -> Yes at 0.359 ($5.00)
- 2026-11-08 coin_flip: Will CS Cienciano vs. CS Huancayo end in a draw? -> Yes at 0.270 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Jeddah be 30°C on November 9? -> No at 0.962 ($5.00)
- 2026-11-08 sure_thing: Exact Score: NK Varaždin 0 - 0 GNK Dinamo Zagreb? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Portland State Vikings vs. Seattle Redhawks -> Portland State Vikings at 0.177 ($5.00)
- 2026-11-08 follow_move: Will Constellation Energy say "Trump" during earnings call? -> No at 0.699 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Shanghai be 10°C on November 9? -> No at 0.711 ($3.55)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
