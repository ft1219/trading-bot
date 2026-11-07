# Polymarket strategy lab (pretend money)

Updated 2026-11-07 01:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 100 | 95/100 | +0.8% | +$3.78 | 2 | 180 | too early |
| 2 | sports_underdog | 134 | 34/134 | -1.5% | -$9.86 | 2 | 66 | too early |
| 3 | fade_move | 58 | 18/58 | -37.2% | -$107.78 | 2 | 96 | too early |
| 4 | follow_move | 43 | 19/43 | -38.5% | -$82.71 | 2 | 96 | too early |
| 5 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 211 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 138 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 48 | 26/48 | +8.8% | +$21.07 | 2 | 232 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | fade_move | follow_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-07 | -$10.33 | -$10.70 | -$13.43 | -$7.43 | +$0.25 | +$13.64 |
| 2026-11-06 | +$14.11 | +$0.84 | -$94.35 | -$75.28 | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Paris Saint-Germain FC vs. ES Troyes AC: O/U 1.5 -> Over at 0.914 ($5.00)
- 2026-11-07 sports_underdog: Will Auckland FC vs. Wellington Phoenix FC end in a draw? -> Yes at 0.280 ($5.00)
- 2026-11-07 fade_move: Dogecoin Up or Down on November 7? -> Up at 0.279 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 7? -> Down at 0.792 ($5.00)
- 2026-11-07 safe_no_week: Will Google (GOOGL) close at <$265 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.942 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Warsaw be 6°C on November 8? -> No at 0.711 ($5.00)
- 2026-11-07 coin_flip: Trail Blazers vs. Lakers: O/U 226.5 -> Under at 0.422 ($5.00)
- 2026-11-07 sure_thing: Hull City AFC leading at halftime? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Spread: Shimizu S-Pulse (-1.5) -> Shimizu S-Pulse at 0.167 ($5.00)
- 2026-11-07 fade_move: Will the price of XRP be between $1.10 and $1.20 on November 9? -> No at 0.386 ($5.00)
- 2026-11-07 follow_move: Will the price of XRP be between $1.10 and $1.20 on November 9? -> Yes at 0.698 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Tel Aviv be 24°C on November 8? -> No at 0.943 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 35 (0 with a problem).
