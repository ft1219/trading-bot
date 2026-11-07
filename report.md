# Polymarket strategy lab (pretend money)

Updated 2026-11-07 16:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 18 | 18/18 | +4.7% | +$4.19 | 2 | 268 | too early |
| 2 | sure_thing | 206 | 198/206 | +2.0% | +$20.57 | 2 | 257 | too early |
| 3 | sports_underdog | 302 | 66/302 | -14.9% | -$222.37 | 2 | 78 | too early |
| 4 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 106 | too early |
| 5 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 114 | too early |
| 6 | weather_forecast | 31 | 9/31 | -55.6% | -$86.16 | 1 | 161 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 125 | 66/125 | +5.9% | +$36.49 | 2 | 339 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | +$3.83 | +$6.46 | -$223.21 | -$10.37 | -$23.43 | -$86.16 | +$29.05 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will Constellation Energy say "Power" 5+ times during earnings call? -> Yes at 0.933 ($5.00)
- 2026-11-07 sure_thing: UT Rio Grande Valley vs. Northwestern State -> UT Rio Grande Valley at 0.922 ($5.00)
- 2026-11-07 sports_underdog: Spread: Bologna FC 1909 (-1.5) -> Bologna FC 1909 at 0.321 ($5.00)
- 2026-11-07 follow_move: Will "Housewife - Tate McRae" be the #1 song this week? -> No at 0.470 ($5.00)
- 2026-11-07 fade_move: Will "Housewife - Tate McRae" be the #1 song this week? -> Yes at 0.592 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Warsaw be 5°C on November 9? -> No at 0.622 ($5.00)
- 2026-11-07 coin_flip: Pau FC vs. FC Nantes: O/U 2.5 -> Under at 0.602 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Buenos Aires be 24°C on November 9? -> No at 0.933 ($5.00)
- 2026-11-07 sure_thing: Spread: Fresno State (-20.5) -> Utah State at 0.932 ($5.00)
- 2026-11-07 sports_underdog: Will Odense BK win on 2026-11-07? -> Yes at 0.341 ($5.00)
- 2026-11-07 follow_move: Will "Housewife - Tate McRae" be the #2 US song this week? -> Yes at 0.769 ($5.00)
- 2026-11-07 fade_move: Will "Housewife - Tate McRae" be the #2 US song this week? -> No at 0.290 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
