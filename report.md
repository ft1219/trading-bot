# Polymarket strategy lab (pretend money)

Updated 2026-11-09 20:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 882 | 814/882 | -1.6% | -$68.98 | 4 | 151 | too early |
| 2 | safe_no_week | 165 | 155/165 | -2.4% | -$19.95 | 4 | 318 | too early |
| 3 | follow_move | 100 | 58/100 | -8.6% | -$43.21 | 4 | 165 | too early |
| 4 | sports_underdog | 765 | 167/765 | -17.7% | -$672.37 | 4 | 60 | too early |
| 5 | weather_forecast | 175 | 89/175 | -23.1% | -$199.33 | 3 | 157 | too early |
| 6 | fade_move | 115 | 32/115 | -47.4% | -$272.72 | 4 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 871 | 439/871 | -2.9% | -$125.69 | 4 | 216 | yardstick |

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
| 2026-11-09 | -$4.57 | -$1.30 | +$13.52 | -$167.41 | -$57.85 | -$89.27 | +$22.95 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: BNB Up or Down - November 9, 3PM ET -> Up at 0.972 ($5.00)
- 2026-11-09 safe_no_week: Will there be 3 earthquakes of 6.5 or above magnitude worldwide? -> No at 0.943 ($5.00)
- 2026-11-09 follow_move: Will the price of XRP be above $1.10 on November 15? -> No at 0.577 ($5.00)
- 2026-11-09 sports_underdog: South Alabama Jaguars vs. UCF Knights (W) -> South Alabama Jaguars at 0.208 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Chongqing be 17°C on November 11? -> No at 0.632 ($5.00)
- 2026-11-09 fade_move: Bitcoin Up or Down on November 10? -> Up at 0.417 ($5.00)
- 2026-11-09 coin_flip: Dogecoin Up or Down - November 11, 9AM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: Will Servette FC Chênois Féminin win on 2026-11-10? -> No at 0.924 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Los Angeles be between 84-85°F on November 11? -> No at 0.943 ($5.00)
- 2026-11-09 follow_move: Will there be 0 earthquakes of 6.5 or above magnitude worldwide? -> Yes at 0.517 ($5.00)
- 2026-11-09 sports_underdog: Syracuse Orange vs. Indiana Hoosiers -> Syracuse Orange at 0.331 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Manila be 32°C on November 11? -> No at 0.592 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (8 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
