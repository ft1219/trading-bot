# Polymarket strategy lab (pretend money)

Updated 2026-11-06 20:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | fade_move | 14 | 8/14 | +21.9% | +$15.30 | 1 | 132 | too early |
| 2 | sure_thing | 31 | 30/31 | +2.5% | +$3.91 | 1 | 193 | too early |
| 3 | sports_underdog | 59 | 14/59 | -12.8% | -$37.20 | 1 | 88 | too early |
| 4 | follow_move | 13 | 5/13 | -37.8% | -$24.57 | 1 | 118 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 188 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 127 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 18 | 8/18 | -18.2% | -$16.42 | 1 | 206 | yardstick |

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
| 2026-11-06 | +$15.30 | +$3.91 | -$37.20 | -$24.57 | +$0.12 | -$16.42 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 fade_move: Will "Clayface" 3rd Weekend Box Office be between 6m and 7m? -> Yes at 0.341 ($5.00)
- 2026-11-06 sure_thing: Spread: Gimhae FC (-1.5) -> Hwaseong FC at 0.924 ($5.00)
- 2026-11-06 sports_underdog: Spread: Internacional de Bogotá (-1.5) -> Internacional de Bogotá at 0.177 ($5.00)
- 2026-11-06 follow_move: Will "Clayface" 3rd Weekend Box Office be between 6m and 7m? -> No at 0.730 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Cape Town be 25°C on November 8? -> No at 0.962 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Helsinki be -1°C on November 7? -> No at 0.740 ($5.00)
- 2026-11-06 coin_flip: Spread: RFK Akhmat Groznyi (-1.5) -> RFK Akhmat Groznyi at 0.331 ($5.00)
- 2026-11-06 fade_move: Will Zelenskyy post 40-59 posts from November 6 to November 13, 2026? -> Yes at 0.177 ($5.00)
- 2026-11-06 sure_thing: Spread: Bristol City FC (-2.5) -> Norwich City FC at 0.952 ($5.00)
- 2026-11-06 sports_underdog: Will CA Unión vs. CA Vélez Sarsfield end in a draw? -> Yes at 0.310 ($5.00)
- 2026-11-06 follow_move: Will Labour Party win the most seats in the New Zealand House of Representatives in the 2026 New Zealand legislative election? -> Yes at 0.431 ($5.00)
- 2026-11-06 safe_no_week: Will the price of Solana be between $70 and $80 on November 13? -> No at 0.963 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 28 (0 with a problem).
