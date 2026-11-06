# Polymarket strategy lab (pretend money)

Updated 2026-11-06 16:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 12 | 12/12 | +5.5% | +$3.33 | 1 | 164 | too early |
| 2 | sports_underdog | 26 | 7/26 | -5.6% | -$7.06 | 1 | 73 | too early |
| 3 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 164 | too early |
| 4 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 109 | too early |
| 5 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 123 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 117 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 8 | 4/8 | -4.5% | -$1.81 | 1 | 168 | yardstick |

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

| Day | sure_thing | sports_underdog | safe_no_week | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-06 | +$3.33 | -$7.06 | +$0.12 | -$5.00 | +$11.37 | -$1.81 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Will Google (GOOGL) finish week of November 2 above $280? -> Yes at 0.971 ($4.86)
- 2026-11-06 sports_underdog: Will Union Brescia vs. FC Arzignano Valchiampo end in a draw? -> Yes at 0.249 ($5.00)
- 2026-11-06 safe_no_week: Will the National Party win 45-49 seats in the New Zealand House of Representatives in the 2026 New Zealand legislative election? -> No at 0.983 ($5.00)
- 2026-11-06 follow_move: Will CZ post 40-59 posts from November 3 to November 10, 2026? -> Yes at 0.482 ($5.00)
- 2026-11-06 fade_move: Will Trump's approval rating be between 38.5 and 38.9 on November 6, 2026? -> Yes at 0.145 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Busan be 14°C on November 8? -> No at 0.661 ($5.00)
- 2026-11-06 coin_flip: Will the price of Ethereum be between $2,200 and $2,300 on November 8? -> Yes at 0.607 ($5.00)
- 2026-11-06 sure_thing: Spread: FC Felgueiras 1932 (-2.5) -> Leixoes SC at 0.960 ($5.00)
- 2026-11-06 sports_underdog: Spread: Union Brescia (-2.5) -> Union Brescia at 0.187 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Jeddah be 30°C on November 8? -> No at 0.983 ($5.00)
- 2026-11-06 follow_move: Will "The One About Matthew Perry: Season 1" be the #2 US Netflix show this week? -> Yes at 0.422 ($5.00)
- 2026-11-06 fade_move: Will CZ post 40-59 posts from November 3 to November 10, 2026? -> No at 0.562 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 22 (0 with a problem).
