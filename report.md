# Polymarket strategy lab (pretend money)

Updated 2026-11-06 04:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 0 | - | - | +$0.00 | 0 | 24 | too early |
| 2 | safe_no_week | 0 | - | - | +$0.00 | 0 | 24 | too early |
| 3 | sports_underdog | 0 | - | - | +$0.00 | 0 | 5 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 24 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 24 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 24 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 0 | - | - | +$0.00 | 0 | 24 | yardstick |

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

- 2026-11-06 sure_thing: Exact Score: Boyacá Chicó FC 0 - 0 Internacional de Bogotá? -> No at 0.914 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Tokyo be 18°C on November 7? -> No at 0.980 ($5.00)
- 2026-11-06 sports_underdog: Counter-Strike: PARIVISION vs Natus Vincere (BO3) - IEM Beijing Playoffs -> PARIVISION at 0.310 ($5.00)
- 2026-11-06 follow_move: Will voter turnout be between 80% and 82% in the 2026 New Zealand general election? -> Yes at 0.521 ($5.00)
- 2026-11-06 fade_move: Will the price of Ethereum be above $2,100 on November 11? -> Yes at 0.837 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Helsinki be 6°C on November 7? -> No at 0.492 ($5.00)
- 2026-11-06 coin_flip: Bitcoin Up or Down - November 6, 12:15AM-12:20AM ET -> Up at 0.527 ($5.00)
- 2026-11-06 sure_thing: Exact Score: Auckland FC 0 - 0 Wellington Phoenix FC? -> No at 0.952 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in London be 9°C on November 7? -> No at 0.934 ($5.00)
- 2026-11-06 sports_underdog: Games Total: O/U 3.5 -> Under at 0.341 ($1.71)
- 2026-11-06 follow_move: Will the price of Bitcoin be less than $72,000 on November 11? -> Yes at 0.186 ($5.00)
- 2026-11-06 fade_move: Solana Up or Down on November 6? -> Up at 0.428 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 3 (0 with a problem).
