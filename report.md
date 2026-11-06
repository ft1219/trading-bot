# Polymarket strategy lab (pretend money)

Updated 2026-11-06 14:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sports_underdog | 15 | 4/15 | -17.3% | -$12.40 | 1 | 60 | too early |
| 2 | sure_thing | 6 | 6/6 | +5.4% | +$1.61 | 1 | 146 | too early |
| 3 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 104 | too early |
| 4 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 117 | too early |
| 5 | safe_no_week | 0 | - | - | +$0.00 | 0 | 146 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 109 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 6 | 3/6 | -4.3% | -$1.29 | 1 | 146 | yardstick |

What each one does:

- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sports_underdog | sure_thing | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|
| 2026-11-06 | -$12.40 | +$1.61 | -$5.00 | +$11.37 | -$1.29 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sports_underdog: Will NK Lokomotiva Zagreb vs. NK Rudeš end in a draw? -> Yes at 0.280 ($5.00)
- 2026-11-06 sure_thing: Exact Score: SV Waldhof Mannheim 07 1 - 0 Fortuna Cologne? -> No at 0.952 ($5.00)
- 2026-11-06 follow_move: S&P 500 (SPY) closes above $745 on November 6? -> No at 0.777 ($5.00)
- 2026-11-06 fade_move: Will Apple (AAPL) close above $345 on November 6? -> Yes at 0.187 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Munich be 5°C on November 8? -> No at 0.971 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Houston be between 64-65°F on November 8? -> No at 0.798 ($5.00)
- 2026-11-06 coin_flip: Dogecoin Up or Down - November 8, 3AM ET -> Down at 0.527 ($5.00)
- 2026-11-06 sports_underdog: Will SG Dynamo Dresden vs. SpVgg Greuther Fürth end in a draw? -> Yes at 0.270 ($5.00)
- 2026-11-06 sure_thing: Will Everton FC win on 2026-11-07? -> No at 0.952 ($5.00)
- 2026-11-06 follow_move: Will Meta (META) close above $620 on November 6? -> Yes at 0.456 ($5.00)
- 2026-11-06 fade_move: Gold (XAUUSD) Up or Down on November 6? -> Up at 0.120 ($5.00)
- 2026-11-06 safe_no_week: Will the price of Bitcoin be between $70,000 and $72,000 on November 9? -> No at 0.975 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 19 (0 with a problem).
