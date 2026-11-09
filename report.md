# Polymarket strategy lab (pretend money)

Updated 2026-11-09 19:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 879 | 811/879 | -1.6% | -$70.11 | 4 | 138 | too early |
| 2 | safe_no_week | 163 | 153/163 | -2.5% | -$20.22 | 4 | 312 | too early |
| 3 | follow_move | 100 | 58/100 | -8.6% | -$43.21 | 4 | 164 | too early |
| 4 | sports_underdog | 758 | 167/758 | -16.9% | -$637.37 | 4 | 58 | too early |
| 5 | weather_forecast | 175 | 89/175 | -23.1% | -$199.33 | 3 | 156 | too early |
| 6 | fade_move | 115 | 32/115 | -47.4% | -$272.72 | 4 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 854 | 427/854 | -3.6% | -$154.62 | 4 | 217 | yardstick |

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
| 2026-11-09 | -$5.69 | -$1.57 | +$13.52 | -$132.41 | -$57.85 | -$89.27 | -$5.98 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Exact Score: CP Mijas-Las Lagunas 0 - 0 Real Jaén CF? -> No at 0.949 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Qingdao be 15°C on November 11? -> No at 0.962 ($5.00)
- 2026-11-09 follow_move: Will there be 0 earthquakes of 6.5 or above magnitude worldwide? -> Yes at 0.517 ($5.00)
- 2026-11-09 sports_underdog: Counter-Strike: your end vs Damajuana (BO3) - CCT South America Group Stage -> Damajuana at 0.290 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Manila be 32°C on November 11? -> No at 0.592 ($5.00)
- 2026-11-09 fade_move: Bitcoin Up or Down on November 10? -> Up at 0.417 ($5.00)
- 2026-11-09 coin_flip: BNB Up or Down - November 9, 8:15PM-8:20PM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: Exact Score: SD Amorebieta 0 - 0 UD Logroñés? -> No at 0.950 ($5.00)
- 2026-11-09 safe_no_week: WTI Crude Oil (WTI) closes above $92 on November 10? -> No at 0.981 ($5.00)
- 2026-11-09 follow_move: Will Palantir Technologies Inc. (PLTR) hit (LOW) $153 Week of November 9 2026? -> No at 0.855 ($5.00)
- 2026-11-09 sports_underdog: Knoxville: Liam Draxl vs Duncan Chan -> Duncan Chan at 0.249 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Buenos Aires be 29°C on November 11? -> No at 0.612 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 37 (6 with a problem).
Latest problem: 5 position(s) still open more than 3 days after their market ended
