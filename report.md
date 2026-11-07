# Polymarket strategy lab (pretend money)

Updated 2026-11-07 08:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 145 | 138/145 | +1.2% | +$8.77 | 2 | 222 | too early |
| 2 | sports_underdog | 200 | 43/200 | -16.0% | -$158.40 | 2 | 84 | too early |
| 3 | follow_move | 44 | 20/44 | -36.7% | -$80.65 | 2 | 100 | too early |
| 4 | fade_move | 59 | 18/59 | -38.2% | -$112.78 | 2 | 102 | too early |
| 5 | weather_forecast | 5 | 2/5 | -37.3% | -$9.32 | 1 | 160 | too early |
| 6 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 240 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 79 | 41/79 | +5.7% | +$22.44 | 2 | 289 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$5.34 | -$159.24 | -$5.37 | -$18.43 | -$9.32 | +$0.25 | +$15.01 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Exact Score: Yunnan Yukun FC 1 - 0 Wuhan San Zhen FC? -> No at 0.971 ($5.00)
- 2026-11-07 sports_underdog: FC Belshina Bobruisk vs. FC Isloch: O/U 1.5 -> Under at 0.257 ($5.00)
- 2026-11-07 follow_move: Will PPI YoY be 6.4% in October? -> Yes at 0.227 ($5.00)
- 2026-11-07 fade_move: Will Khamenei post 0-4 posts from November 6 to November 13, 2026? -> No at 0.270 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Ankara be 8°C on November 9? -> No at 0.681 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Miami be between 88-89°F on November 9? -> No at 0.962 ($5.00)
- 2026-11-07 coin_flip: Will Al Ain FC win on 2026-11-08? -> Yes at 0.562 ($5.00)
- 2026-11-07 sure_thing: Exact Score: FC Machida Zelvia 0 - 0 Sanfrecce Hiroshima? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Spread: Perth Glory FC (-1.5) -> Perth Glory FC at 0.218 ($5.00)
- 2026-11-07 follow_move: Will Khamenei post 0-4 posts from November 6 to November 13, 2026? -> Yes at 0.759 ($5.00)
- 2026-11-07 fade_move: Will PPI YoY be 6.4% in October? -> No at 0.833 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Kuala Lumpur be 33°C on November 9? -> No at 0.750 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: SBV Excelsior vs. Go Ahead Eagles - First Team to Score (yes), 1.005 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
