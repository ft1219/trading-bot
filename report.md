# Polymarket strategy lab (pretend money)

Updated 2026-11-09 14:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 840 | 774/840 | -2.2% | -$93.16 | 4 | 127 | too early |
| 2 | safe_no_week | 131 | 122/131 | -3.2% | -$21.03 | 4 | 311 | too early |
| 3 | follow_move | 80 | 42/80 | -15.1% | -$60.38 | 4 | 167 | too early |
| 4 | sports_underdog | 748 | 165/748 | -16.5% | -$613.42 | 4 | 26 | too early |
| 5 | weather_forecast | 151 | 74/151 | -25.6% | -$191.35 | 3 | 165 | too early |
| 6 | fade_move | 95 | 30/95 | -40.7% | -$193.46 | 4 | 179 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 798 | 398/798 | -4.3% | -$169.78 | 4 | 209 | yardstick |

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
| 2026-11-09 | -$28.75 | -$2.38 | -$3.66 | -$108.47 | -$49.88 | -$10.00 | -$21.14 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-09 sure_thing: Ethereum above 2,140 on November 9, 10AM ET? -> No at 0.925 ($5.00)
- 2026-11-09 safe_no_week: Will Solana reach $100 November 9-15? -> No at 0.944 ($5.00)
- 2026-11-09 follow_move: Rocket Lab (RKLB) Up or Down on November 9? -> Up at 0.659 ($5.00)
- 2026-11-09 sports_underdog: KHL: CSKA Moscow vs. Sibir Novosibirsk -> Sibir Novosibirsk at 0.270 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Panama City be 34°C or higher on November 11? -> No at 0.808 ($5.00)
- 2026-11-09 fade_move: Rocket Lab (RKLB) Up or Down on November 9? -> Down at 0.413 ($5.00)
- 2026-11-09 coin_flip: XRP Up or Down - November 9, 7:50PM-7:55PM ET -> Down at 0.527 ($5.00)
- 2026-11-09 sure_thing: Meta (META) Up or Down on November 9? -> Up at 0.913 ($5.00)
- 2026-11-09 safe_no_week: Will XRP reach $1.30 November 9-15? -> No at 0.963 ($5.00)
- 2026-11-09 follow_move: Gold (XAUUSD) Up or Down on November 9? -> Up at 0.845 ($5.00)
- 2026-11-09 sports_underdog: BNP Paribas Nordic Open: Tomas Etcheverry vs Max Dahlin -> Max Dahlin at 0.218 ($5.00)
- 2026-11-09 weather_forecast: Will the highest temperature in Toronto be 13°C on November 11? -> No at 0.818 ($4.30)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Vietnam vs. Chinese Taipei (yes), 1.001 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
