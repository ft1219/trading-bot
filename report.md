# Polymarket strategy lab (pretend money)

Updated 2026-11-09 08:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 810 | 748/810 | -2.0% | -$81.89 | 4 | 111 | too early |
| 2 | safe_no_week | 121 | 112/121 | -3.8% | -$23.00 | 4 | 295 | too early |
| 3 | follow_move | 79 | 41/79 | -15.6% | -$61.73 | 4 | 150 | too early |
| 4 | sports_underdog | 743 | 164/743 | -16.1% | -$595.98 | 4 | 13 | too early |
| 5 | weather_forecast | 145 | 73/145 | -23.4% | -$167.77 | 3 | 158 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 162 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 740 | 372/740 | -3.4% | -$125.82 | 4 | 196 | yardstick |

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
| 2026-11-09 | -$17.47 | -$4.36 | -$5.00 | -$91.03 | -$26.30 |  | +$22.82 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Will XRP reach $1.15 on November 9? -> No at 0.916 ($5.00)
- 2026-11-09 safe_no_week: Will Netflix (NFLX) finish week of November 9 above $60? -> Yes at 0.933 ($5.00)
- 2026-11-09 follow_move: Will the price of Solana be between $70 and $80 on November 14? -> No at 0.849 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: Froglings vs Team Synapse (BO3) - DreamLeague Division 2 Group A -> Team Synapse at 0.352 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Milan be 11°C on November 11? -> No at 0.856 ($5.00)
- 2026-11-09 fade_move: Will the price of Solana be between $70 and $80 on November 14? -> Yes at 0.222 ($5.00)
- 2026-11-09 coin_flip: Bitcoin Up or Down - November 9, 4:40AM-4:45AM ET -> Up at 0.527 ($5.00)
- 2026-11-09 sure_thing: Bitcoin above 73,200 on November 9, 4AM ET? -> Yes at 0.972 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Denver be between 64-65°F on November 10? -> No at 0.981 ($5.00)
- 2026-11-09 follow_move: Will NVIDIA (NVDA) finish week of November 9 above $170? -> No at 0.369 ($5.00)
- 2026-11-09 sports_underdog: Dota 2: Power Rangers vs Nemiga Gaming (BO3) - DreamLeague Division 2 Group A -> Nemiga Gaming at 0.280 ($5.00)
- 2026-11-09 weather_forecast: Will the lowest temperature in Guangzhou be 11°C on November 11? -> Yes at 0.142 ($3.97)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
