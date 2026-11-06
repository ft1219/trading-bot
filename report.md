# Polymarket strategy lab (pretend money)

Updated 2026-11-06 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 2 | 2/2 | +3.5% | +$0.35 | 1 | 54 | too early |
| 2 | sports_underdog | 1 | 1/1 | +184.7% | +$9.24 | 1 | 13 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 56 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 55 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 56 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 56 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 2 | 2/2 | +91.4% | +$9.14 | 1 | 54 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | coin_flip |
|---|---|---|---|
| 2026-11-06 | +$0.35 | +$9.24 | +$9.14 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Jazz vs. Mavericks: O/U 205.5 -> Over at 0.914 ($5.00)
- 2026-11-06 sports_underdog: Taipei: Coleman Wong vs Kasidit Samrej -> Kasidit Samrej at 0.167 ($5.00)
- 2026-11-06 safe_no_week: Will Nikolajus Lebedevičius win the 2026 Northern Nalšia district by-election? -> No at 0.986 ($5.00)
- 2026-11-06 follow_move: Will SpaceX (SPCX) finish week of November 2 above $120? -> No at 0.207 ($5.00)
- 2026-11-06 fade_move: Will "Godzilla Minus Zero" Opening Weekend Box Office be less than 28m? -> Yes at 0.187 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Panama City be 30°C on November 7? -> No at 0.612 ($5.00)
- 2026-11-06 coin_flip: Will OGC Nice win on 2026-11-08? -> No at 0.542 ($5.00)
- 2026-11-06 sure_thing: Spread: Auckland FC (-2.5) -> Wellington Phoenix FC at 0.924 ($5.00)
- 2026-11-06 sports_underdog: Counter-Strike: FURIA vs BetBoom Team (BO3) - IEM Beijing Playoffs -> BetBoom Team at 0.361 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Chongqing be 17°C on November 7? -> No at 0.933 ($5.00)
- 2026-11-06 follow_move: Will White House post 180-199 posts from November 3 to November 10, 2026? -> Yes at 0.373 ($5.00)
- 2026-11-06 fade_move: Will WTI Crude Oil (WTI) hit (HIGH) $95 Week of November 2 2026? -> No at 0.787 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 7 (0 with a problem).
