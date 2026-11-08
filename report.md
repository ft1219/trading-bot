# Polymarket strategy lab (pretend money)

Updated 2026-11-08 09:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 462 | 434/462 | -0.4% | -$9.07 | 3 | 201 | too early |
| 2 | safe_no_week | 49 | 47/49 | -0.5% | -$1.17 | 3 | 285 | too early |
| 3 | sports_underdog | 507 | 115/507 | -13.5% | -$339.39 | 3 | 69 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 121 | too early |
| 5 | weather_forecast | 76 | 36/76 | -26.2% | -$98.56 | 2 | 168 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 129 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 364 | 183/364 | -1.5% | -$27.90 | 3 | 300 | yardstick |

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
| 2026-11-08 | +$2.64 | -$2.44 | -$97.29 |  | +$8.72 | +$1.40 | -$88.26 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Independiente Santa Fe vs. AD Pasto: O/U 1.5 -> Over at 0.904 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Guangzhou be 20°C on November 10? -> No at 0.934 ($5.00)
- 2026-11-08 sports_underdog: Spread: Stabaek IF (-1.5) -> Stabaek IF at 0.270 ($5.00)
- 2026-11-08 follow_move: Will Meta Platforms, Inc. (META) hit (HIGH) $630 Week of November 9 2026? -> Yes at 0.625 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Milan be 11°C on November 10? -> No at 0.740 ($5.00)
- 2026-11-08 fade_move: Ethereum Up or Down on November 8? -> Down at 0.417 ($5.00)
- 2026-11-08 coin_flip: Ceará SC vs. América FC: Draw at halftime? -> No at 0.602 ($5.00)
- 2026-11-08 sure_thing: Rasisalai United vs. Bangkok United FC: O/U 0.5 -> Over at 0.965 ($5.00)
- 2026-11-08 safe_no_week: Will "A Dog's Perfect Christmas" be the #2 US Netflix movie this week? -> No at 0.961 ($5.00)
- 2026-11-08 sports_underdog: Spread: Sumqayit FK (-1.5) -> Sumqayit FK at 0.198 ($5.00)
- 2026-11-08 follow_move: Ethereum Up or Down on November 8? -> Up at 0.627 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Milan be 8°C on November 10? -> Yes at 0.164 ($3.93)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
