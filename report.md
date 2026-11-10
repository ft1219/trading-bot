# Polymarket strategy lab (pretend money)

Updated 2026-11-10 14:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1054 | 975/1054 | -1.3% | -$67.86 | 5 | 135 | too early |
| 2 | safe_no_week | 214 | 202/214 | -1.7% | -$17.92 | 5 | 347 | too early |
| 3 | follow_move | 136 | 83/136 | -2.1% | -$13.99 | 5 | 156 | too early |
| 4 | sports_underdog | 873 | 198/873 | -15.4% | -$666.49 | 5 | 32 | too early |
| 5 | weather_forecast | 218 | 105/218 | -27.7% | -$297.73 | 4 | 167 | too early |
| 6 | fade_move | 155 | 45/155 | -33.5% | -$259.61 | 5 | 167 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1088 | 535/1088 | -5.8% | -$314.90 | 5 | 207 | yardstick |

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
| 2026-11-10 | -$5.08 | +$6.01 | +$31.68 | +$20.46 | -$79.84 | -$9.16 | -$192.75 |
| 2026-11-09 | +$1.64 | -$5.28 | +$11.06 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: XRP Up or Down on November 10? -> Down at 0.963 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Shenzhen be 26°C on November 12? -> No at 0.924 ($5.00)
- 2026-11-10 follow_move: S&P 500 (SPY) closes above $750 on November 10? -> Yes at 0.430 ($5.00)
- 2026-11-10 sports_underdog: Monastir: Jay Clarke vs Maxime Janvier -> Maxime Janvier at 0.338 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Chongqing be 15°C on November 12? -> No at 0.701 ($5.00)
- 2026-11-10 fade_move: Will Apple (AAPL) close above $350 on November 10? -> No at 0.299 ($5.00)
- 2026-11-10 coin_flip: Counter-Strike: UPGRADE vs Butterfly (BO3) - NODWIN Clutch Series Group Stage -> Butterfly at 0.472 ($5.00)
- 2026-11-10 sure_thing: Will the price of XRP be between $1.00 and $1.10 on November 10? -> Yes at 0.938 ($5.00)
- 2026-11-10 safe_no_week: Will Tesla (TSLA) close above $390 on November 11? -> No at 0.933 ($5.00)
- 2026-11-10 follow_move: S&P 500 (SPX) Up or Down on November 10? -> Down at 0.767 ($5.00)
- 2026-11-10 sports_underdog: Cleveland State Vikings vs. Drake Bulldogs (W) -> Cleveland State Vikings at 0.259 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Denver be between 42-43°F on November 11? -> Yes at 0.161 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (34 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
