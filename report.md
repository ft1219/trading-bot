# Polymarket strategy lab (pretend money)

Updated 2026-11-09 22:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 910 | 841/910 | -1.4% | -$65.78 | 4 | 137 | too early |
| 2 | safe_no_week | 179 | 168/179 | -2.4% | -$21.70 | 4 | 307 | too early |
| 3 | follow_move | 120 | 72/120 | -4.7% | -$28.36 | 4 | 145 | too early |
| 4 | sports_underdog | 772 | 169/772 | -17.6% | -$676.29 | 4 | 69 | too early |
| 5 | weather_forecast | 181 | 91/181 | -23.9% | -$213.46 | 3 | 151 | too early |
| 6 | fade_move | 138 | 39/138 | -40.2% | -$277.58 | 4 | 156 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 887 | 448/887 | -2.8% | -$122.64 | 4 | 216 | yardstick |

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
| 2026-11-09 | -$1.36 | -$3.05 | +$28.36 | -$171.34 | -$71.99 | -$94.13 | +$26.00 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Ethereum above 2,140 on November 9, 6PM ET? -> No at 0.963 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Moscow be 5°C on November 11? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will the price of XRP be above $1.10 on November 15? -> No at 0.577 ($5.00)
- 2026-11-09 sports_underdog: Western Illinois Leathernecks vs. Omaha Mavericks (W) -> Omaha Mavericks at 0.287 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Chongqing be 17°C on November 11? -> No at 0.632 ($5.00)
- 2026-11-09 fade_move: Bitcoin Up or Down on November 10? -> Up at 0.417 ($5.00)
- 2026-11-09 coin_flip: ZCash Up or Down - November 10, 5:35AM-5:40AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Hyperliquid Up or Down - November 9, 5:00PM-5:15PM ET -> Down at 0.953 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Jeddah be 30°C on November 11? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will there be 0 earthquakes of 6.5 or above magnitude worldwide? -> Yes at 0.517 ($5.00)
- 2026-11-09 sports_underdog: Will Club Aurora vs. FC Universitario end in a draw? -> Yes at 0.259 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Manila be 32°C on November 11? -> No at 0.592 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (10 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
