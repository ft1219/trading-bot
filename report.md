# Polymarket strategy lab (pretend money)

Updated 2026-11-10 03:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 135 | 83/135 | -1.3% | -$8.99 | 5 | 134 | too early |
| 2 | sure_thing | 982 | 907/982 | -1.5% | -$73.96 | 5 | 117 | too early |
| 3 | safe_no_week | 198 | 186/198 | -2.1% | -$21.23 | 5 | 301 | too early |
| 4 | sports_underdog | 820 | 184/820 | -15.9% | -$649.04 | 5 | 42 | too early |
| 5 | weather_forecast | 200 | 98/200 | -26.2% | -$258.26 | 4 | 137 | too early |
| 6 | fade_move | 154 | 44/154 | -34.2% | -$262.81 | 5 | 144 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 964 | 479/964 | -4.7% | -$224.78 | 5 | 203 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | +$36.68 | -$11.18 | +$2.70 | +$37.91 | -$40.38 | -$12.36 | -$102.63 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Ethereum Up or Down on November 10? -> Down at 0.617 ($5.00)
- 2026-11-10 sure_thing: Bitcoin Up or Down - November 9, 8:00PM-12:00AM ET -> Down at 0.926 ($5.00)
- 2026-11-10 safe_no_week: Will "Victorian Psycho" score at least 60 on the Rotten Tomatoes Tomatometer? -> Yes at 0.943 ($5.00)
- 2026-11-10 sports_underdog: Matsuyama: Rei Sakamoto vs Renta Tokuda -> Renta Tokuda at 0.167 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Austin be between 76-77°F on November 11? -> No at 0.622 ($5.00)
- 2026-11-10 fade_move: Ethereum Up or Down on November 10? -> Up at 0.427 ($5.00)
- 2026-11-10 coin_flip: Ethereum Up or Down - November 10, 3:10PM-3:15PM ET -> Down at 0.527 ($5.00)
- 2026-11-10 follow_move: Solana Up or Down on November 10? -> Down at 0.617 ($5.00)
- 2026-11-10 sure_thing: Magic vs. Kings: O/U 199.5 -> Over at 0.924 ($5.00)
- 2026-11-10 safe_no_week: Will the lowest temperature in Miami be between 72-73°F on November 11? -> No at 0.944 ($5.00)
- 2026-11-10 sports_underdog: Matsuyama: Shintaro Imai vs Fajing Sun -> Shintaro Imai at 0.341 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Shanghai be 19°C on November 11? -> No at 0.759 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (18 with a problem).
Latest problem: 6 position(s) still open more than 3 days after their market ended
