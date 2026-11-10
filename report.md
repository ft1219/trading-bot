# Polymarket strategy lab (pretend money)

Updated 2026-11-10 17:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 152 | 94/152 | +1.5% | +$11.37 | 5 | 163 | too early |
| 2 | sure_thing | 1078 | 997/1078 | -1.3% | -$70.61 | 5 | 139 | too early |
| 3 | safe_no_week | 243 | 230/243 | -1.4% | -$16.83 | 5 | 341 | too early |
| 4 | sports_underdog | 885 | 200/885 | -15.8% | -$693.50 | 5 | 58 | too early |
| 5 | weather_forecast | 238 | 116/238 | -27.0% | -$315.99 | 4 | 159 | too early |
| 6 | fade_move | 172 | 49/172 | -29.8% | -$256.01 | 5 | 174 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1118 | 546/1118 | -6.5% | -$361.66 | 5 | 217 | yardstick |

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
| 2026-11-10 | +$57.03 | -$7.83 | +$7.10 | -$6.56 | -$98.10 | -$5.55 | -$239.51 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Will CZ post 20-39 posts from November 10 to November 17, 2026? -> No at 0.562 ($5.00)
- 2026-11-10 sure_thing: Hyperliquid Up or Down - November 10, 12:15PM-12:30PM ET -> Up at 0.963 ($5.00)
- 2026-11-10 safe_no_week: Will the price of Bitcoin be above $66,000 on November 17? -> Yes at 0.963 ($5.00)
- 2026-11-10 sports_underdog: UE Tavernes vs. Valencia CF: O/U 4.5 -> Under at 0.218 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Houston be between 64-65°F on November 11? -> No at 0.701 ($5.00)
- 2026-11-10 fade_move: Will the price of Ethereum be between $1,800 and $1,900 on November 16? -> Yes at 0.169 ($5.00)
- 2026-11-10 coin_flip: Solana Up or Down - November 11, 6:50AM-6:55AM ET -> Up at 0.527 ($5.00)
- 2026-11-10 follow_move: Will Airbnb, Inc. (ABNB) hit (LOW) $180 Week of November 9 2026? -> Yes at 0.440 ($5.00)
- 2026-11-10 sure_thing: Will the price of Bitcoin be above $70,000 on November 11? -> Yes at 0.960 ($5.00)
- 2026-11-10 safe_no_week: Will the price of Ethereum be above $1,800 on November 17? -> Yes at 0.944 ($5.00)
- 2026-11-10 sports_underdog: Will Paris Saint-Germain FC win on 2026-11-10? -> Yes at 0.239 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Madrid be 18°C on November 12? -> No at 0.750 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 1.003 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
