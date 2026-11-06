# Polymarket strategy lab (pretend money)

Updated 2026-11-06 03:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 0 | - | - | +$0.00 | 0 | 16 | too early |
| 2 | safe_no_week | 0 | - | - | +$0.00 | 0 | 16 | too early |
| 3 | sports_underdog | 0 | - | - | +$0.00 | 0 | 4 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 16 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 16 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 16 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 0 | - | - | +$0.00 | 0 | 16 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

No trades have finished yet.

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Spread: Derby County FC (-2.5) -> Bolton Wanderers FC at 0.943 ($5.00)
- 2026-11-06 safe_no_week: Will Zelenskyy post 120-139 posts from November 3 to November 10, 2026? -> No at 0.981 ($5.00)
- 2026-11-06 sports_underdog: Games Total: O/U 3.5 -> Under at 0.341 ($1.71)
- 2026-11-06 follow_move: Will the price of Bitcoin be between $74,000 and $76,000 on November 6? -> Yes at 0.437 ($5.00)
- 2026-11-06 fade_move: Will the price of XRP be above $1.20 on November 7? -> Yes at 0.601 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Shenzhen be 25°C on November 7? -> No at 0.691 ($5.00)
- 2026-11-06 coin_flip: Qingdao Hainiu FC vs. Shenzhen Xinpengcheng FC: 1st Half O/U 0.5 -> Over at 0.808 ($5.00)
- 2026-11-06 sure_thing: Spread: FC Petrolul Ploieşti (-1.5) -> FC UTA Arad at 0.943 ($5.00)
- 2026-11-06 safe_no_week: Will the price of XRP be above $1.40 on November 12? -> No at 0.972 ($5.00)
- 2026-11-06 sports_underdog: Heat vs. Warriors: O/U 227.5 -> Under at 0.351 ($5.00)
- 2026-11-06 follow_move: Will the price of Bitcoin be above $74,000 on November 8? -> No at 0.180 ($5.00)
- 2026-11-06 fade_move: Will the price of Ethereum be above $2,200 on November 8? -> Yes at 0.697 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 2 (0 with a problem).
