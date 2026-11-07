# Polymarket strategy lab (pretend money)

Updated 2026-11-07 10:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 158 | 150/158 | +0.9% | +$7.45 | 2 | 225 | too early |
| 2 | sports_underdog | 229 | 51/229 | -12.1% | -$137.14 | 2 | 71 | too early |
| 3 | follow_move | 44 | 20/44 | -36.7% | -$80.65 | 2 | 100 | too early |
| 4 | fade_move | 59 | 18/59 | -38.2% | -$112.78 | 2 | 102 | too early |
| 5 | weather_forecast | 9 | 2/9 | -65.2% | -$29.32 | 1 | 160 | too early |
| 6 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 248 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 83 | 44/83 | +5.2% | +$21.31 | 2 | 301 | yardstick |

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
| 2026-11-07 | -$6.66 | -$137.98 | -$5.37 | -$18.43 | -$29.32 | +$0.25 | +$13.88 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Preston North End FC vs. Southampton FC: Neither team to score first? -> No at 0.960 ($5.00)
- 2026-11-07 sports_underdog: Will FC Ingolstadt 04 vs. Fortuna Dusseldorf end in a draw? -> Yes at 0.280 ($5.00)
- 2026-11-07 follow_move: Will PPI YoY be 6.4% in October? -> Yes at 0.227 ($5.00)
- 2026-11-07 fade_move: Will Khamenei post 0-4 posts from November 6 to November 13, 2026? -> No at 0.270 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Wellington be 15°C on November 8? -> No at 0.567 ($5.00)
- 2026-11-07 safe_no_week: Will the lowest temperature in Tokyo be 13°C on November 8? -> No at 0.971 ($5.00)
- 2026-11-07 coin_flip: Shanghai Shenhua FC vs. Qingdao Xihaian FC: Shanghai Shenhua FC O/U 2.5 -> Over at 0.482 ($5.00)
- 2026-11-07 sure_thing: St Johnstone FC vs. Dundee FC: Neither team to score first? -> No at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Spread: Samsunspor (-1.5) -> Samsunspor at 0.218 ($5.00)
- 2026-11-07 follow_move: Will Khamenei post 0-4 posts from November 6 to November 13, 2026? -> Yes at 0.759 ($5.00)
- 2026-11-07 fade_move: Will PPI YoY be 6.4% in October? -> No at 0.833 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Beijing be -5°C or below on November 9? -> No at 0.818 ($5.00)

## Price gaps seen today

1 near-gaps recorded (full sets within a few cents of their payout). Cheapest: SBV Excelsior vs. Go Ahead Eagles - First Team to Score (yes), 1.005 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
