# Polymarket strategy lab (pretend money)

Updated 2026-11-06 18:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | fade_move | 12 | 8/12 | +42.2% | +$25.30 | 1 | 124 | too early |
| 2 | sure_thing | 17 | 17/17 | +5.7% | +$4.85 | 1 | 175 | too early |
| 3 | sports_underdog | 39 | 9/39 | -18.6% | -$35.73 | 1 | 76 | too early |
| 4 | follow_move | 11 | 3/11 | -60.3% | -$33.17 | 1 | 111 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 180 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 121 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 9 | 5/9 | +6.1% | +$2.77 | 1 | 183 | yardstick |

What each one does:

- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | fade_move | sure_thing | sports_underdog | follow_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-06 | +$25.30 | +$4.85 | -$35.73 | -$33.17 | +$0.12 | +$2.77 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 fade_move: Solana Up or Down on November 7? -> Up at 0.428 ($5.00)
- 2026-11-06 sure_thing: Spread: Volos NPS (-2.5) -> AE Kifisia FC at 0.971 ($5.00)
- 2026-11-06 sports_underdog: Will Montpellier HSC vs. FC Metz end in a draw? -> Yes at 0.259 ($5.00)
- 2026-11-06 follow_move: XRP Up or Down on November 7? -> Down at 0.689 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Kuala Lumpur be 31°C on November 8? -> No at 0.952 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Panama City be 31°C on November 8? -> No at 0.652 ($5.00)
- 2026-11-06 coin_flip: Spread: Texas Tech (-30.5) -> Texas Tech at 0.218 ($5.00)
- 2026-11-06 fade_move: XRP Up or Down on November 7? -> Up at 0.361 ($5.00)
- 2026-11-06 sure_thing: Spread: Dundee United FC (-2.5) -> Motherwell FC at 0.904 ($5.00)
- 2026-11-06 sports_underdog: Will CA Grau vs. Cusco FC end in a draw? -> Yes at 0.280 ($5.00)
- 2026-11-06 follow_move: Will "You Seem Pretty Sad for a Girl So in Love - Olivia Rodrigo" be the Billboard 200 #1 album for the week of November 14? -> No at 0.522 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Sao Paulo be 22°C on November 8? -> No at 0.924 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 24 (0 with a problem).
