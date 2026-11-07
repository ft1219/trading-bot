# Polymarket strategy lab (pretend money)

Updated 2026-11-07 18:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | safe_no_week | 24 | 24/24 | +4.4% | +$5.23 | 2 | 271 | too early |
| 2 | sure_thing | 249 | 239/249 | +1.8% | +$21.79 | 2 | 238 | too early |
| 3 | sports_underdog | 321 | 69/321 | -16.5% | -$262.91 | 2 | 83 | too early |
| 4 | follow_move | 59 | 31/59 | -23.0% | -$67.78 | 2 | 96 | too early |
| 5 | fade_move | 74 | 21/74 | -45.7% | -$169.18 | 2 | 106 | too early |
| 6 | weather_forecast | 31 | 9/31 | -55.6% | -$86.16 | 1 | 165 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 157 | 87/157 | +7.4% | +$57.62 | 2 | 331 | yardstick |

What each one does:

- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | safe_no_week | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | +$4.87 | +$7.68 | -$263.74 | +$7.49 | -$74.83 | -$86.16 | +$50.18 |
| 2026-11-06 | +$0.37 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 safe_no_week: Will Brian Thomas Jr.'s next team be the San Francisco 49ers? -> No at 0.952 ($5.00)
- 2026-11-07 sure_thing: Exact Score: Viking FK 1 - 0 KFUM-Kameratene Oslo? -> No at 0.943 ($5.00)
- 2026-11-07 sports_underdog: Spread: Deportivo Tachira (-1.5) -> Deportivo Tachira at 0.280 ($5.00)
- 2026-11-07 follow_move: Will the price of XRP be above $1.20 on November 13? -> No at 0.724 ($5.00)
- 2026-11-07 fade_move: Will the price of Bitcoin be above $80,000 on November 13? -> Yes at 0.147 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in New York City be between 50-51°F on November 9? -> No at 0.691 ($5.00)
- 2026-11-07 coin_flip: Colorado vs. Arizona State: O/U 35.5 -> Under at 0.225 ($5.00)
- 2026-11-07 safe_no_week: Will UKMTO publish 12-15 notices between November 2-November 8? -> No at 0.970 ($5.00)
- 2026-11-07 sure_thing: Spread: Kalmar FF (-2.5) -> IK Sirius at 0.971 ($5.00)
- 2026-11-07 sports_underdog: Bethune-Cookman vs. Southern University: O/U 57.5 -> Over at 0.357 ($5.00)
- 2026-11-07 follow_move: Will the price of Ethereum be between $2,100 and $2,200 on November 12? -> No at 0.802 ($5.00)
- 2026-11-07 fade_move: Will the price of Ethereum be between $2,000 and $2,100 on November 13? -> Yes at 0.127 ($5.00)

## Price gaps seen today

9 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
