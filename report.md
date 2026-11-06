# Polymarket strategy lab (pretend money)

Updated 2026-11-06 08:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 3 | 3/3 | +3.3% | +$0.50 | 1 | 77 | too early |
| 2 | sports_underdog | 3 | 1/3 | -5.1% | -$0.76 | 1 | 20 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 80 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 69 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 72 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 80 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 4 | 2/4 | -4.3% | -$0.86 | 1 | 76 | yardstick |

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
| 2026-11-06 | +$0.50 | -$0.76 | -$0.86 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Spread: Qarabag FK (-3.5) -> Turan Tovuz at 0.952 ($5.00)
- 2026-11-06 sports_underdog: Counter-Strike: Copenhagen Wolves vs Passion Academy (BO3) - United21 Group D -> Passion Academy at 0.290 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Shanghai be 18°C on November 7? -> No at 0.959 ($5.00)
- 2026-11-06 follow_move: Will Silver (XAGUSD) hit (HIGH) $54 Week of November 2 2026? -> No at 0.826 ($5.00)
- 2026-11-06 fade_move: Will Zelenskyy post 80-99 posts from October 30 to November 6, 2026? -> No at 0.241 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Karachi be 37°C on November 7? -> No at 0.482 ($5.00)
- 2026-11-06 coin_flip: Spread: North Carolina (-8.5) -> UConn at 0.567 ($5.00)
- 2026-11-06 sure_thing: Exact Score: Seongnam Ilhwa 0 - 0 Daegu FC? -> No at 0.954 ($5.00)
- 2026-11-06 sports_underdog: Chennai Open: Robin Montgomery vs Maaya Rajeshwaran Revathi -> Maaya Rajeshwaran Revathi at 0.187 ($5.00)
- 2026-11-06 safe_no_week: Will monthly inflation increase by 0.1% or less in October? -> No at 0.952 ($5.00)
- 2026-11-06 follow_move: Will the price of Ethereum be between $2,100 and $2,200 on November 9? -> Yes at 0.343 ($5.00)
- 2026-11-06 fade_move: Will the price of Bitcoin be between $78,000 and $80,000 on November 9? -> Yes at 0.169 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 10 (0 with a problem).
