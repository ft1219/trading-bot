# Polymarket strategy lab (pretend money)

Updated 2026-11-06 08:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 3 | 3/3 | +3.3% | +$0.50 | 1 | 69 | too early |
| 2 | sports_underdog | 3 | 1/3 | -5.1% | -$0.76 | 1 | 19 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 72 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 64 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 68 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 72 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 2 | 2/2 | +91.4% | +$9.14 | 1 | 70 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | coin_flip |
|---|---|---|---|
| 2026-11-06 | +$0.50 | -$0.76 | +$9.14 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Will NVIDIA (NVDA) finish week of November 2 above $205? -> No at 0.971 ($5.00)
- 2026-11-06 sports_underdog: Chennai Open: Robin Montgomery vs Maaya Rajeshwaran Revathi -> Maaya Rajeshwaran Revathi at 0.187 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in San Francisco be between 64-65°F on November 7? -> No at 0.984 ($5.00)
- 2026-11-06 follow_move: Will the price of Ethereum be between $2,200 and $2,300 on November 6? -> Yes at 0.676 ($5.00)
- 2026-11-06 fade_move: Will the price of XRP be above $1.30 on November 11? -> Yes at 0.127 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in New York City be between 60-61°F on November 7? -> No at 0.522 ($5.00)
- 2026-11-06 coin_flip: XRP Up or Down - November 6, 1:30PM-1:45PM ET -> Up at 0.527 ($5.00)
- 2026-11-06 sure_thing: Exact Score: Ascoli Calcio 1898 FC 0 - 0 Palermo FC? -> No at 0.950 ($5.00)
- 2026-11-06 sports_underdog: Spread: FK Livyi Bereh (-1.5) -> FK Livyi Bereh at 0.177 ($5.00)
- 2026-11-06 safe_no_week: Will the lowest temperature in Tokyo be 14°C on November 7? -> No at 0.933 ($5.00)
- 2026-11-06 follow_move: Will "Godzilla Minus Zero" Opening Weekend Box Office be less than 28m? -> No at 0.850 ($5.00)
- 2026-11-06 fade_move: BNB Up or Down on November 6? -> Up at 0.453 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 9 (0 with a problem).
