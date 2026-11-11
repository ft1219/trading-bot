# Polymarket strategy lab (pretend money)

Updated 2026-11-11 09:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 187 | 114/187 | +0.6% | +$5.99 | 6 | 152 | too early |
| 2 | sure_thing | 1255 | 1166/1255 | -0.4% | -$24.84 | 6 | 113 | too early |
| 3 | safe_no_week | 304 | 286/304 | -1.9% | -$29.37 | 6 | 329 | too early |
| 4 | sports_underdog | 986 | 226/986 | -14.6% | -$714.65 | 6 | 24 | too early |
| 5 | fade_move | 208 | 63/208 | -23.8% | -$247.41 | 6 | 168 | too early |
| 6 | weather_forecast | 286 | 143/286 | -25.4% | -$356.60 | 5 | 156 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1300 | 638/1300 | -6.0% | -$388.72 | 6 | 227 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-11 | -$4.19 | +$53.86 | -$2.79 | -$89.65 | +$1.91 | -$37.56 | -$51.97 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will the price of Ethereum be between $1,900 and $2,000 on November 16? -> No at 0.821 ($5.00)
- 2026-11-11 sure_thing: Will Meta (META) close above $630 on November 11? -> Yes at 0.942 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Miami be between 84-85°F on November 13? -> No at 0.971 ($5.00)
- 2026-11-11 sports_underdog: Spread: Vietnam (-1.5) -> Chinese Taipei at 0.280 ($5.00)
- 2026-11-11 fade_move: Will the price of Bitcoin be between $70,000 and $72,000 on November 16? -> Yes at 0.201 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Shenzhen be 27°C on November 13? -> No at 0.701 ($5.00)
- 2026-11-11 coin_flip: Ethereum Up or Down - November 11, 7:15AM-7:20AM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will the price of Bitcoin be between $70,000 and $72,000 on November 16? -> No at 0.830 ($5.00)
- 2026-11-11 sure_thing: DAX (DAX) Up or Down on November 11? -> Up at 0.922 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Chengdu be 17°C on November 13? -> No at 0.924 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: Nexus vs MOUZ NXT (BO3) - CCT Europe Group Stage -> MOUZ NXT at 0.249 ($5.00)
- 2026-11-11 fade_move: Will Amedeo Modigliani's “Tête” sell for at least $43m at auction? -> Yes at 0.218 ($5.00)

## Price gaps seen today

4 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.999 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
