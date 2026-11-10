# Polymarket strategy lab (pretend money)

Updated 2026-11-10 04:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1003 | 926/1003 | -1.5% | -$74.91 | 5 | 107 | too early |
| 2 | follow_move | 136 | 83/136 | -2.1% | -$13.99 | 5 | 134 | too early |
| 3 | safe_no_week | 198 | 186/198 | -2.1% | -$21.23 | 5 | 304 | too early |
| 4 | sports_underdog | 840 | 190/840 | -15.3% | -$638.33 | 5 | 27 | too early |
| 5 | weather_forecast | 200 | 98/200 | -26.2% | -$258.26 | 4 | 139 | too early |
| 6 | fade_move | 155 | 45/155 | -33.5% | -$259.61 | 5 | 144 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 989 | 488/989 | -5.3% | -$262.85 | 5 | 194 | yardstick |

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
| 2026-11-10 | -$12.13 | +$31.68 | +$2.70 | +$48.61 | -$40.38 | -$9.16 | -$140.70 |
| 2026-11-09 | +$1.64 | +$11.06 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | +$16.06 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$2.49 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | -$75.28 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Ethereum Up or Down - November 9, 11PM ET -> Up at 0.953 ($5.00)
- 2026-11-10 follow_move: XRP Up or Down on November 10? -> Down at 0.636 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Sao Paulo be 25°C on November 11? -> No at 0.924 ($5.00)
- 2026-11-10 sports_underdog: Brisbane 3: Christian Langmo vs Ymerali Ibraimi -> Ymerali Ibraimi at 0.173 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Seattle be between 52-53°F on November 11? -> No at 0.652 ($5.00)
- 2026-11-10 fade_move: XRP Up or Down on November 10? -> Up at 0.423 ($5.00)
- 2026-11-10 coin_flip: ZCash Up or Down - November 10, 6:45AM-7:00AM ET -> Down at 0.527 ($5.00)
- 2026-11-10 sure_thing: Gold Up or Down - November 9, 11:00PM-12:00AM ET -> Up at 0.617 ($5.00)
- 2026-11-10 follow_move: Ethereum Up or Down on November 10? -> Down at 0.617 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Warsaw be 2°C on November 11? -> No at 0.981 ($5.00)
- 2026-11-10 sports_underdog: Matsuyama: Ryuki Matsuda vs Max Schoenhaus -> Ryuki Matsuda at 0.187 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Karachi be 33°C on November 11? -> No at 0.612 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (20 with a problem).
Latest problem: 6 position(s) still open more than 3 days after their market ended
