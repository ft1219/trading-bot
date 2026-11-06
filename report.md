# Polymarket strategy lab (pretend money)

Updated 2026-11-06 22:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 70 | 68/70 | +3.0% | +$10.54 | 1 | 178 | too early |
| 2 | sports_underdog | 92 | 23/92 | -8.9% | -$40.65 | 1 | 79 | too early |
| 3 | follow_move | 38 | 17/38 | -37.1% | -$70.28 | 1 | 98 | too early |
| 4 | fade_move | 49 | 15/49 | -39.6% | -$96.91 | 1 | 103 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 205 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 129 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 35 | 19/35 | +5.6% | +$9.83 | 1 | 213 | yardstick |

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
| 2026-11-06 | +$10.54 | -$40.65 | -$70.28 | -$96.91 | +$0.12 | +$9.83 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Exact Score: South Shields 1 - 0 Southport FC? -> No at 0.933 ($5.00)
- 2026-11-06 sports_underdog: North Carolina A&T Aggies vs. Marshall Thundering Herd (W) -> North Carolina A&T Aggies at 0.187 ($5.00)
- 2026-11-06 follow_move: Will Pixelworks (PXLW) beat quarterly earnings? -> No at 0.800 ($5.00)
- 2026-11-06 fade_move: Ethereum Up or Down on November 7? -> Down at 0.386 ($5.00)
- 2026-11-06 safe_no_week: Will the lowest temperature in New York City be between 46-47°F on November 8? -> No at 0.972 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Dallas be between 68-69°F on November 8? -> No at 0.602 ($5.00)
- 2026-11-06 coin_flip: Colchester United FC vs. Worcester City FC: Colchester United FC O/U 2.5 -> Over at 0.453 ($5.00)
- 2026-11-06 sure_thing: Spread: Aberdeen FC (-2.5) -> Hibernian FC at 0.943 ($5.00)
- 2026-11-06 sports_underdog: Thunder vs. Grizzlies: O/U 216.5 -> Under at 0.361 ($5.00)
- 2026-11-06 follow_move: Will the National Party win 35-39 seats in the New Zealand House of Representatives in the 2026 New Zealand legislative election? -> Yes at 0.550 ($5.00)
- 2026-11-06 fade_move: Will Pixelworks (PXLW) beat quarterly earnings? -> Yes at 0.239 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Los Angeles be between 90-91°F on November 8? -> No at 0.986 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 31 (0 with a problem).
