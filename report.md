# Polymarket strategy lab (pretend money)

Updated 2026-11-08 16:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 517 | 487/517 | -0.1% | -$2.87 | 3 | 226 | too early |
| 2 | safe_no_week | 55 | 52/55 | -1.8% | -$5.06 | 3 | 303 | too early |
| 3 | sports_underdog | 576 | 129/576 | -15.0% | -$429.73 | 3 | 80 | too early |
| 4 | weather_forecast | 84 | 42/84 | -21.7% | -$89.89 | 2 | 177 | too early |
| 5 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 125 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 136 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 441 | 225/441 | -1.3% | -$27.81 | 3 | 303 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | sports_underdog | weather_forecast | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$8.85 | -$6.32 | -$187.63 | +$17.38 |  | +$1.40 | -$88.17 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | +$2.49 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 |  | -$75.28 | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Exact Score: Raja Club Athletic 0 - 0 IR Tanger? -> No at 0.914 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Chongqing be 17°C on November 10? -> No at 0.924 ($5.00)
- 2026-11-08 sports_underdog: Spread: Sheffield Wednesday FC (-1.5) -> Sheffield Wednesday FC at 0.290 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Seoul (Incheon) be 4°C on November 10? -> No at 0.798 ($5.00)
- 2026-11-08 follow_move: Will Trump's approval rating be at least 39.0 on November 13, 2026? -> No at 0.550 ($5.00)
- 2026-11-08 fade_move: Will Trump's approval rating be at least 39.0 on November 13, 2026? -> Yes at 0.500 ($5.00)
- 2026-11-08 coin_flip: Incarnate Word Cardinals vs. UTEP Miners: O/U 141.5 -> Under at 0.512 ($5.00)
- 2026-11-08 sure_thing: Will Gençlerbirliği SK win on 2026-11-08? -> No at 0.952 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Panama City be 35°C or higher on November 10? -> No at 0.943 ($5.00)
- 2026-11-08 sports_underdog: Spread: Club Alianza Lima (-1.5) -> Club Alianza Lima at 0.321 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Shanghai be 16°C on November 10? -> No at 0.642 ($5.00)
- 2026-11-08 follow_move: Will the White House call a full lid by 6:30 PM on November 9? -> No at 0.460 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
