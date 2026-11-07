# Polymarket strategy lab (pretend money)

Updated 2026-11-07 04:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 117 | 110/117 | -0.2% | -$1.06 | 2 | 202 | too early |
| 2 | sports_underdog | 165 | 37/165 | -12.7% | -$103.80 | 2 | 75 | too early |
| 3 | follow_move | 44 | 20/44 | -36.7% | -$80.65 | 2 | 96 | too early |
| 4 | fade_move | 59 | 18/59 | -38.2% | -$112.78 | 2 | 98 | too early |
| 5 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 217 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 141 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 64 | 33/64 | +6.6% | +$20.82 | 2 | 256 | yardstick |

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
| 2026-11-07 | -$15.17 | -$104.64 | -$5.37 | -$18.43 | +$0.25 | +$13.39 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: RCD Espanyol de Barcelona vs. RC Deportivo A Coruña: Neither team to score first? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Spread: Guandong GZ-Power FC (-1.5) -> Guandong GZ-Power FC at 0.321 ($5.00)
- 2026-11-07 follow_move: Will UK GDP growth in Q3 2026 be between 0.6% and 0.7%? -> Yes at 0.575 ($5.00)
- 2026-11-07 fade_move: Will CZ post 0-19 posts from November 6 to November 13, 2026? -> Yes at 0.130 ($5.00)
- 2026-11-07 safe_no_week: Will NVIDIA (NVDA) finish week of November 9 above $165? -> Yes at 0.952 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Los Angeles be between 64-65°F on November 8? -> No at 0.877 ($5.00)
- 2026-11-07 coin_flip: Will AS FAR vs. Difaâ Hassani El Jadida end in a draw? -> Yes at 0.229 ($5.00)
- 2026-11-07 sure_thing: West Bromwich Albion FC vs. Millwall FC: Neither team to score first? -> No at 0.971 ($4.86)
- 2026-11-07 sports_underdog: Spread: Shenzhen Juniors FC (-1.5) -> Shenzhen Juniors FC at 0.208 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 7? -> Down at 0.792 ($5.00)
- 2026-11-07 fade_move: Will UK GDP growth in Q3 2026 be between 0.6% and 0.7%? -> No at 0.475 ($5.00)
- 2026-11-07 safe_no_week: Will the price of XRP be between $0.90 and $1.00 on November 13? -> No at 0.985 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
