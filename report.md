# Polymarket strategy lab (pretend money)

Updated 2026-11-07 00:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 98 | 93/98 | +0.6% | +$2.83 | 2 | 174 | too early |
| 2 | sports_underdog | 131 | 33/131 | -2.1% | -$13.40 | 2 | 64 | too early |
| 3 | follow_move | 41 | 19/41 | -35.5% | -$72.71 | 2 | 98 | too early |
| 4 | fade_move | 55 | 16/55 | -43.4% | -$119.35 | 2 | 99 | too early |
| 5 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 208 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 137 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 48 | 26/48 | +8.8% | +$21.07 | 2 | 224 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-07 | -$11.28 | -$14.24 | +$2.57 | -$25.00 | +$0.25 | +$13.64 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Exact Score: FC Cajamarca 0 - 0 Club Alianza Atlético? -> No at 0.962 ($5.00)
- 2026-11-07 sports_underdog: Tarleton State Texans vs. San Diego Toreros -> Tarleton State Texans at 0.280 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 7? -> Down at 0.792 ($5.00)
- 2026-11-07 fade_move: Dogecoin Up or Down on November 7? -> Up at 0.279 ($5.00)
- 2026-11-07 safe_no_week: S&P 500 (SPY) closes above $720 on November 9? -> Yes at 0.962 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Lucknow be 17°C on November 8? -> No at 0.750 ($5.00)
- 2026-11-07 coin_flip: Bitcoin Up or Down - November 7, 11AM ET -> Up at 0.524 ($5.00)
- 2026-11-07 sure_thing: Spread: Blackburn Rovers FC (-1.5) -> West Ham United FC at 0.952 ($5.00)
- 2026-11-07 sports_underdog: Rainbow Six Siege: TYLOO vs All Gamers (BO3) - BLAST R6 Major Osaka Phase 1 -> TYLOO at 0.218 ($5.00)
- 2026-11-07 follow_move: Will the price of XRP be between $1.10 and $1.20 on November 9? -> Yes at 0.698 ($5.00)
- 2026-11-07 fade_move: Will the price of XRP be between $1.10 and $1.20 on November 9? -> No at 0.386 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Houston be between 62-63°F on November 8? -> No at 0.925 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 34 (0 with a problem).
