# Polymarket strategy lab (pretend money)

Updated 2026-11-07 15:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 188 | 180/188 | +1.6% | +$15.38 | 2 | 259 | too early |
| 2 | sports_underdog | 280 | 65/280 | -9.4% | -$130.24 | 2 | 84 | too early |
| 3 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 103 | too early |
| 4 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 112 | too early |
| 5 | weather_forecast | 15 | 3/15 | -67.2% | -$50.43 | 1 | 175 | too early |
| 6 | safe_no_week | 9 | 9/9 | +4.5% | +$2.03 | 2 | 269 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 114 | 61/114 | +7.1% | +$39.98 | 2 | 334 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | +$1.27 | -$131.08 | -$10.37 | -$23.43 | -$50.43 | +$1.66 | +$32.54 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Exact Score: Imisli FK 0 - 0 Sumqayit FK? -> No at 0.933 ($5.00)
- 2026-11-07 sports_underdog: Costa do Sauipe: Gonzalo Bueno vs Camilo Ugo Carabelli -> Gonzalo Bueno at 0.259 ($5.00)
- 2026-11-07 follow_move: NVIDIA (NVDA) Up or Down on November 9? -> Up at 0.629 ($5.00)
- 2026-11-07 fade_move: NVIDIA (NVDA) Up or Down on November 9? -> Down at 0.435 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Busan be 14°C on November 9? -> No at 0.642 ($5.00)
- 2026-11-07 safe_no_week: Will Microsoft (MSFT) close at $490-$500 on the final day of trading of the week of Nov 9 – Nov 13? -> No at 0.981 ($5.00)
- 2026-11-07 coin_flip: Dogecoin Up or Down - November 8, 4:30AM-4:35AM ET -> Up at 0.527 ($5.00)
- 2026-11-07 sure_thing: Brighton & Hove Albion FC vs. Brentford FC: Neither team to score first? -> No at 0.968 ($5.00)
- 2026-11-07 sports_underdog: Spread: Norfolk State (-3.5) -> Norfolk State at 0.306 ($5.00)
- 2026-11-07 follow_move: Will NVIDIA (NVDA) close above $195 on November 9? -> No at 0.845 ($5.00)
- 2026-11-07 fade_move: Will Amazon (AMZN) close above $250 on November 9? -> No at 0.159 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Qingdao be 11°C on November 9? -> No at 0.691 ($5.00)

## Price gaps seen today

7 near-gaps recorded (full sets within a few cents of their payout). Cheapest: October Inflation China - Annual (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
