# Polymarket strategy lab (pretend money)

Updated 2026-11-06 12:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sports_underdog | 10 | 2/10 | -20.5% | -$9.56 | 1 | 46 | too early |
| 2 | sure_thing | 6 | 6/6 | +5.4% | +$1.61 | 1 | 122 | too early |
| 3 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 82 | too early |
| 4 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 93 | too early |
| 5 | safe_no_week | 0 | - | - | +$0.00 | 0 | 128 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 101 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 6 | 3/6 | -4.3% | -$1.29 | 1 | 122 | yardstick |

What each one does:

- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sports_underdog | sure_thing | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|
| 2026-11-06 | -$9.56 | +$1.61 | -$5.00 | +$11.37 | -$1.29 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sports_underdog: Chennai Open: Mai Hontama vs Magda Linette -> Mai Hontama at 0.331 ($5.00)
- 2026-11-06 sure_thing: Spread: Pelicans (-12.5) -> Timberwolves at 0.914 ($5.00)
- 2026-11-06 follow_move: Will Cerebras Systems (CBRS) beat quarterly earnings? -> No at 0.856 ($5.00)
- 2026-11-06 fade_move: Will the Labour Party win 30-34 seats in the New Zealand House of Representatives in the 2026 New Zealand legislative election? -> Yes at 0.370 ($5.00)
- 2026-11-06 safe_no_week: Will the price of Solana be between $100 and $110 on November 12? -> No at 0.953 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Atlanta be between 70-71°F on November 8? -> No at 0.750 ($5.00)
- 2026-11-06 coin_flip: Spread: Arizona (-5.5) -> TCU at 0.427 ($5.00)
- 2026-11-06 sports_underdog: Spread: FC UTA Arad (-1.5) -> FC UTA Arad at 0.280 ($5.00)
- 2026-11-06 sure_thing: Exact Score: VfL Osnabrück 0 - 0 1. FC Kaiserslautern? -> No at 0.946 ($5.00)
- 2026-11-06 follow_move: Will Meta Platforms, Inc. (META) hit (LOW) $580 Week of November 2 2026? -> Yes at 0.278 ($5.00)
- 2026-11-06 fade_move: Will Meta Platforms, Inc. (META) hit (LOW) $580 Week of November 2 2026? -> No at 0.855 ($5.00)
- 2026-11-06 safe_no_week: Will Google have the second highest OpenRouter market share the week of November 2? -> No at 0.983 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 16 (0 with a problem).
