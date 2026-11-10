# Polymarket strategy lab (pretend money)

Updated 2026-11-10 21:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 178 | 109/178 | +1.2% | +$11.00 | 5 | 145 | too early |
| 2 | safe_no_week | 260 | 246/260 | -1.4% | -$18.69 | 5 | 338 | too early |
| 3 | sure_thing | 1126 | 1039/1126 | -1.6% | -$88.01 | 5 | 131 | too early |
| 4 | sports_underdog | 906 | 205/906 | -15.5% | -$698.21 | 5 | 57 | too early |
| 5 | fade_move | 197 | 59/197 | -26.5% | -$260.92 | 5 | 158 | too early |
| 6 | weather_forecast | 243 | 119/243 | -26.7% | -$319.28 | 4 | 162 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1152 | 563/1152 | -6.3% | -$361.79 | 5 | 231 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | safe_no_week | sure_thing | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | +$56.66 | +$5.24 | -$25.23 | -$11.27 | -$10.47 | -$101.40 | -$239.64 |
| 2026-11-09 | +$11.06 | -$5.28 | +$1.64 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$19.92 | -$52.70 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | +$0.90 | -$25.83 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$0.37 | +$14.11 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 follow_move: Will Donald Trump post 200+ Truth Social posts from November 10 to November 17, 2026? -> No at 0.856 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Denver be between 64-65°F on November 12? -> No at 0.971 ($5.00)
- 2026-11-10 sure_thing: Ethereum above 2,070 on November 10, 5PM ET? -> No at 0.963 ($5.00)
- 2026-11-10 sports_underdog: Capitals vs. Senators: O/U 4.5 -> Under at 0.218 ($5.00)
- 2026-11-10 fade_move: Will Donald Trump post 200+ Truth Social posts from November 10 to November 17, 2026? -> Yes at 0.185 ($5.00)
- 2026-11-10 weather_forecast: Will the lowest temperature in Shanghai be 14°C on November 12? -> No at 0.661 ($5.00)
- 2026-11-10 coin_flip: Louisiana-Monroe Warhawks vs. TCU Horned Frogs: O/U 160.5 -> Under at 0.532 ($5.00)
- 2026-11-10 follow_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> No at 0.738 ($5.00)
- 2026-11-10 safe_no_week: Will the lowest temperature in Miami be between 68-69°F on November 12? -> No at 0.952 ($5.00)
- 2026-11-10 sure_thing: Juventus FC vs. OL Lyonnes: O/U 1.5 -> Over at 0.924 ($5.00)
- 2026-11-10 sports_underdog: Winthrop Eagles vs. Kennesaw State Owls -> Winthrop Eagles at 0.187 ($5.00)
- 2026-11-10 fade_move: Will OpenRouter process between 220T and 230T tokens the week of November 9? -> Yes at 0.329 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
