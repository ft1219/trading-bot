# Polymarket strategy lab (pretend money)

Updated 2026-11-10 00:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 944 | 872/944 | -1.5% | -$71.25 | 5 | 120 | too early |
| 2 | follow_move | 133 | 81/133 | -1.6% | -$10.82 | 5 | 134 | too early |
| 3 | safe_no_week | 192 | 180/192 | -2.4% | -$22.76 | 5 | 299 | too early |
| 4 | sports_underdog | 796 | 175/796 | -17.5% | -$692.51 | 5 | 61 | too early |
| 5 | weather_forecast | 194 | 97/194 | -24.6% | -$235.94 | 4 | 142 | too early |
| 6 | fade_move | 152 | 44/152 | -33.3% | -$252.81 | 5 | 144 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 921 | 463/921 | -3.4% | -$157.77 | 5 | 206 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | follow_move | safe_no_week | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | -$8.47 | +$34.85 | +$1.18 | -$5.57 | -$18.05 | -$2.36 | -$35.62 |
| 2026-11-09 | +$1.64 | +$11.06 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | +$16.06 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$2.49 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | -$75.28 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Maine Black Bears vs. Rhode Island Rams -> Rhode Island Rams at 0.971 ($5.00)
- 2026-11-10 follow_move: BNB Up or Down on November 10? -> Up at 0.685 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Toronto be 10°C on November 11? -> No at 0.952 ($5.00)
- 2026-11-10 sports_underdog: Brisbane 3: Dane Sweeny vs Anton Shepp -> Anton Shepp at 0.331 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Shanghai be 19°C on November 11? -> No at 0.759 ($5.00)
- 2026-11-10 fade_move: BNB Up or Down on November 10? -> Down at 0.388 ($5.00)
- 2026-11-10 coin_flip: Will Italy win on 2026-11-12? -> No at 0.808 ($5.00)
- 2026-11-10 sure_thing: Devils vs. Jets: O/U 2.5 -> Over at 0.971 ($5.00)
- 2026-11-09 follow_move: Will there be ≤6 earthquakes of 5.5 or above magnitude worldwide? -> Yes at 0.392 ($5.00)
- 2026-11-09 safe_no_week: Will "BbY WOW - KAROL G, Judeline, rusowsky" be the #1 song this week? -> Yes at 0.962 ($5.00)
- 2026-11-10 sports_underdog: Islanders vs. Sharks: O/U 4.5 -> Under at 0.218 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in London be 8°C on November 11? -> No at 0.562 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (13 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
