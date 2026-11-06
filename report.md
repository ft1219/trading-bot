# Polymarket strategy lab (pretend money)

Updated 2026-11-06 19:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | fade_move | 14 | 8/14 | +21.9% | +$15.30 | 1 | 128 | too early |
| 2 | sure_thing | 23 | 23/23 | +5.7% | +$6.56 | 1 | 185 | too early |
| 3 | sports_underdog | 49 | 13/49 | -7.1% | -$17.19 | 1 | 82 | too early |
| 4 | follow_move | 13 | 5/13 | -37.8% | -$24.57 | 1 | 115 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 184 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 124 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 12 | 6/12 | -9.1% | -$5.48 | 1 | 196 | yardstick |

What each one does:

- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | fade_move | sure_thing | sports_underdog | follow_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-06 | +$15.30 | +$6.56 | -$17.19 | -$24.57 | +$0.12 | -$5.48 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 fade_move: Bitcoin Up or Down on November 7? -> Up at 0.407 ($5.00)
- 2026-11-06 sure_thing: St. Thomas (MN) Tommies vs. Minnesota Golden Gophers -> Minnesota Golden Gophers at 0.933 ($5.00)
- 2026-11-06 sports_underdog: Spread: Cambridge United FC (-1.5) -> Cambridge United FC at 0.208 ($5.00)
- 2026-11-06 follow_move: Will "FRESH" first week sales be at least 120k? -> No at 0.769 ($5.00)
- 2026-11-06 safe_no_week: Will "FRESH" first week sales be at least 160k? -> No at 0.962 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Austin be between 62-63°F on November 8? -> No at 0.671 ($5.00)
- 2026-11-06 coin_flip: Real Sociedad de Fútbol vs. Rayo Vallecano de Madrid: 1st Half O/U 5.5 Total Corners -> Under at 0.642 ($5.00)
- 2026-11-06 fade_move: BNB Up or Down on November 7? -> Up at 0.396 ($5.00)
- 2026-11-06 sure_thing: Exact Score: Oud-Heverlee Leuven 0 - 0 Yellow-Red KV Mechelen? -> No at 0.943 ($5.00)
- 2026-11-06 sports_underdog: Costa do Sauipe: Gonzalo Bueno vs Lautaro Midon -> Gonzalo Bueno at 0.361 ($5.00)
- 2026-11-06 follow_move: Bitcoin Up or Down on November 7? -> Down at 0.636 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Miami be between 82-83°F on November 8? -> No at 0.924 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 26 (0 with a problem).
