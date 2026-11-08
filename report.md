# Polymarket strategy lab (pretend money)

Updated 2026-11-08 23:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 715 | 662/715 | -1.8% | -$64.42 | 3 | 113 | too early |
| 2 | safe_no_week | 94 | 87/94 | -4.0% | -$18.65 | 3 | 287 | too early |
| 3 | follow_move | 78 | 41/78 | -14.6% | -$56.73 | 3 | 127 | too early |
| 4 | sports_underdog | 674 | 150/674 | -15.1% | -$504.95 | 3 | 70 | too early |
| 5 | weather_forecast | 122 | 61/122 | -23.5% | -$141.47 | 2 | 149 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 141 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 641 | 317/641 | -4.6% | -$148.64 | 3 | 191 | yardstick |

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
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Exact Score: Sportivo San Lorenzo 0 - 0 Rubio Nu? -> No at 0.952 ($5.00)
- 2026-11-08 safe_no_week: Will Applied Materials say "Forecast" during earnings call? -> Yes at 0.942 ($5.00)
- 2026-11-08 follow_move: Will Apple (AAPL) close above $340 on November 9? -> Yes at 0.787 ($5.00)
- 2026-11-08 sports_underdog: Penguins vs. Ducks: O/U 5.5 -> Under at 0.321 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Jeddah be 33°C on November 10? -> No at 0.730 ($5.00)
- 2026-11-08 fade_move: Will the price of XRP be between $1.20 and $1.30 on November 10? -> Yes at 0.138 ($5.00)
- 2026-11-08 coin_flip: Dogecoin Up or Down - November 9, 8:20AM-8:25AM ET -> Down at 0.527 ($5.00)
- 2026-11-08 sure_thing: Counter-Strike: HAVU vs BOJONG (BO3) - Elisa Open Suomi Group Stage -> HAVU at 0.933 ($5.00)
- 2026-11-08 safe_no_week: Will Cisco say "Security" 15+ times during earnings call? -> Yes at 0.923 ($5.00)
- 2026-11-08 follow_move: Will Cisco say "Quantum" during earnings call? -> No at 0.420 ($5.00)
- 2026-11-08 sports_underdog: Will Club León FC win on 2026-11-08? -> Yes at 0.280 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Dallas be between 76-77°F on November 10? -> No at 0.711 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
