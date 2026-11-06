# Polymarket strategy lab (pretend money)

Updated 2026-11-06 02:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 0 | - | - | +$0.00 | 0 | 8 | too early |
| 2 | safe_no_week | 0 | - | - | +$0.00 | 0 | 8 | too early |
| 3 | sports_underdog | 0 | - | - | +$0.00 | 0 | 3 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 8 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 8 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 8 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 0 | - | - | +$0.00 | 0 | 8 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

No trades have finished yet.

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Will Bitcoin dip to $75,000 on November 5? -> No at 0.969 ($5.00)
- 2026-11-06 safe_no_week: Will "Black Doves: Season 2" be the top US Netflix show this week? -> No at 0.978 ($5.00)
- 2026-11-06 sports_underdog: Heat vs. Warriors: O/U 227.5 -> Under at 0.351 ($5.00)
- 2026-11-06 follow_move: Will Elon Musk post 40-64 tweets from November 5 to November 7, 2026? -> Yes at 0.382 ($5.00)
- 2026-11-06 fade_move: Will Elon Musk post 280-299 tweets from October 30 to November 6, 2026? -> No at 0.305 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Munich be 8°C on November 7? -> No at 0.691 ($5.00)
- 2026-11-06 coin_flip: Atalanta BC U23 vs. Reggiana 1919: O/U 2.5 -> Over at 0.602 ($5.00)
- 2026-11-06 sure_thing: Spread: Thunder (-19.5) -> Grizzlies at 0.933 ($5.00)
- 2026-11-06 safe_no_week: Will Argentina's monthly inflation in October 2026 be between 2.2% and 2.4%? -> No at 0.961 ($5.00)
- 2026-11-06 sports_underdog: Will Alacranes de Durango vs. Leones Negros UDEG end in a draw? -> Yes at 0.300 ($5.00)
- 2026-11-06 follow_move: Will the Labour Party win 30-34 seats in the New Zealand House of Representatives in the 2026 New Zealand legislative election? -> Yes at 0.479 ($5.00)
- 2026-11-06 fade_move: Will Elon Musk post 40-64 tweets from November 5 to November 7, 2026? -> No at 0.661 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 1 (0 with a problem).
