# Polymarket strategy lab (pretend money)

Updated 2026-11-10 09:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1034 | 957/1034 | -1.2% | -$63.76 | 5 | 120 | too early |
| 2 | safe_no_week | 211 | 199/211 | -1.8% | -$18.63 | 5 | 322 | too early |
| 3 | follow_move | 136 | 83/136 | -2.1% | -$13.99 | 5 | 137 | too early |
| 4 | sports_underdog | 858 | 195/858 | -14.8% | -$630.96 | 5 | 23 | too early |
| 5 | weather_forecast | 215 | 102/215 | -28.7% | -$304.92 | 4 | 146 | too early |
| 6 | fade_move | 155 | 45/155 | -33.5% | -$259.61 | 5 | 148 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1041 | 511/1041 | -5.9% | -$307.39 | 5 | 198 | yardstick |

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
| 2026-11-10 | -$0.98 | +$5.31 | +$31.68 | +$55.98 | -$87.03 | -$9.16 | -$185.24 |
| 2026-11-09 | +$1.64 | -$5.28 | +$11.06 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Will Tesla (TSLA) close above $360 on November 10? -> Yes at 0.971 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Helsinki be 4°C on November 12? -> No at 0.984 ($5.00)
- 2026-11-10 follow_move: Will Ethereum dip to $2,000 November 9-15? -> No at 0.636 ($5.00)
- 2026-11-10 sports_underdog: Counter-Strike: ex-Zero Tenacity vs ILLYRIANS (BO3) - CCT Europe Group Stage -> ILLYRIANS at 0.351 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Singapore be 32°C on November 12? -> No at 0.730 ($5.00)
- 2026-11-10 fade_move: Will the White House call a full lid by 6:30 PM on November 12? -> No at 0.218 ($5.00)
- 2026-11-10 coin_flip: Will StubHub (STUB) beat quarterly earnings? -> Yes at 0.290 ($5.00)
- 2026-11-10 sure_thing: Will Google (GOOGL) close above $300 on November 10? -> No at 0.968 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Paris be 9°C on November 12? -> No at 0.986 ($5.00)
- 2026-11-10 follow_move: Will Bitcoin dip to $72,000 November 9-15? -> No at 0.607 ($5.00)
- 2026-11-10 sports_underdog: Monastir: Federico Bondioli vs Jonas Forejtek -> Federico Bondioli at 0.361 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Shenzhen be 27°C on November 12? -> No at 0.632 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (27 with a problem).
Latest problem: 6 position(s) still open more than 3 days after their market ended
