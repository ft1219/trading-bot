# Polymarket strategy lab (pretend money)

Updated 2026-11-09 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 806 | 744/806 | -2.1% | -$83.69 | 4 | 103 | too early |
| 2 | safe_no_week | 116 | 107/116 | -4.2% | -$24.37 | 4 | 288 | too early |
| 3 | follow_move | 79 | 41/79 | -15.6% | -$61.73 | 4 | 144 | too early |
| 4 | sports_underdog | 740 | 163/740 | -16.2% | -$595.22 | 4 | 13 | too early |
| 5 | weather_forecast | 138 | 69/138 | -23.9% | -$163.15 | 3 | 153 | too early |
| 6 | fade_move | 93 | 30/93 | -39.5% | -$183.46 | 3 | 156 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 728 | 365/728 | -3.6% | -$131.75 | 4 | 192 | yardstick |

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
| 2026-11-09 | -$19.27 | -$5.72 | -$5.00 | -$90.27 | -$21.67 |  | +$16.89 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Solana Up or Down on November 9? -> Down at 0.925 ($5.00)
- 2026-11-09 safe_no_week: Will the lowest temperature in London be 8°C on November 10? -> No at 0.981 ($5.00)
- 2026-11-09 follow_move: Will Elon Musk post 40-64 tweets from November 9 to November 11, 2026? -> Yes at 0.270 ($5.00)
- 2026-11-09 sports_underdog: Counter-Strike: FORZE Reload vs maybe (BO3) - CCT Europe Group Stage -> maybe at 0.331 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Chengdu be 15°C on November 11? -> No at 0.572 ($5.00)
- 2026-11-09 fade_move: Will Elon Musk post 40-64 tweets from November 9 to November 11, 2026? -> No at 0.779 ($5.00)
- 2026-11-09 coin_flip: Solana Up or Down - November 9, 12:50PM-12:55PM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: Ethereum Up or Down - November 9, 12:00AM-4:00AM ET -> Down at 0.953 ($5.00)
- 2026-11-09 safe_no_week: Will the highest temperature in Seoul (Incheon) be 13°C on November 11? -> No at 0.933 ($5.00)
- 2026-11-09 follow_move: S&P 500 (SPX) Opens Up or Down on November 9? -> Up at 0.845 ($5.00)
- 2026-11-09 sports_underdog: Rainbow Six Siege: Fluxo W7M vs EDward Gaming (BO3) - BLAST R6 Major Osaka Phase 2 -> EDward Gaming at 0.187 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Tel Aviv be 21°C on November 11? -> Yes at 0.099 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
