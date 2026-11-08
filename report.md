# Polymarket strategy lab (pretend money)

Updated 2026-11-08 10:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 463 | 435/463 | -0.4% | -$8.85 | 3 | 216 | too early |
| 2 | safe_no_week | 49 | 47/49 | -0.5% | -$1.17 | 3 | 288 | too early |
| 3 | sports_underdog | 513 | 115/513 | -14.5% | -$369.39 | 3 | 79 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 122 | too early |
| 5 | weather_forecast | 76 | 36/76 | -26.2% | -$98.56 | 2 | 170 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 130 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 373 | 189/373 | -0.9% | -$16.03 | 3 | 307 | yardstick |

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
| 2026-11-08 | +$2.87 | -$2.44 | -$127.29 |  | +$8.72 | +$1.40 | -$76.39 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Will UKMTO publish 8-11 notices between November 2-November 8? -> Yes at 0.940 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Singapore be 29°C on November 10? -> No at 0.981 ($5.00)
- 2026-11-08 sports_underdog: Spread: HJK Helsinki (-3.5) -> HJK Helsinki at 0.239 ($5.00)
- 2026-11-08 follow_move: Will IShowSpeed win Best IRL Streamer at the 2026 Streamer Awards? -> Yes at 0.827 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Madrid be 18°C on November 10? -> No at 0.612 ($5.00)
- 2026-11-08 fade_move: Will IShowSpeed win Best IRL Streamer at the 2026 Streamer Awards? -> No at 0.310 ($5.00)
- 2026-11-08 coin_flip: Green Bay Phoenix vs. St. Thomas (MN) Tommies: O/U 151.5 -> Over at 0.462 ($5.00)
- 2026-11-08 sure_thing: Spread: Villarreal CF B (-3.5) -> Juventud Torremolinos CF at 0.904 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Busan be 19°C on November 10? -> No at 0.978 ($5.00)
- 2026-11-08 sports_underdog: Spread: Sandnes Ulf (-2.5) -> Sandnes Ulf at 0.300 ($5.00)
- 2026-11-08 follow_move: Will Meta Platforms, Inc. (META) hit (HIGH) $630 Week of November 9 2026? -> Yes at 0.625 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Beijing be 3°C or higher on November 10? -> Yes at 0.264 ($2.64)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
