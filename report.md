# Polymarket strategy lab (pretend money)

Updated 2026-11-08 18:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 577 | 542/577 | -0.4% | -$11.59 | 3 | 189 | too early |
| 2 | safe_no_week | 78 | 73/78 | -2.9% | -$11.29 | 3 | 287 | too early |
| 3 | sports_underdog | 604 | 134/604 | -15.5% | -$463.99 | 3 | 76 | too early |
| 4 | follow_move | 74 | 38/74 | -22.7% | -$84.00 | 3 | 117 | too early |
| 5 | weather_forecast | 103 | 51/103 | -23.6% | -$120.21 | 2 | 159 | too early |
| 6 | fade_move | 90 | 29/90 | -40.8% | -$183.57 | 3 | 130 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 499 | 248/499 | -4.4% | -$109.80 | 3 | 269 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | sports_underdog | follow_move | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$0.12 | -$12.56 | -$221.89 | -$11.21 | -$12.94 | -$16.33 | -$170.16 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: L.R. Vicenza vs. US Cremonese: Neither team to score first? -> No at 0.933 ($5.00)
- 2026-11-08 safe_no_week: Will the price of Bitcoin be between $70,000 and $72,000 on November 15? -> No at 0.981 ($5.00)
- 2026-11-08 sports_underdog: Spread: CA Nacional Potosí (-1.5) -> CA Nacional Potosí at 0.208 ($5.00)
- 2026-11-08 follow_move: Will "Housewife - Tate McRae" be the #2 song this week? -> Yes at 0.612 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Paris be 3°C on November 9? -> No at 0.623 ($5.00)
- 2026-11-08 fade_move: Will the price of Ethereum be between $2,200 and $2,300 on November 14? -> Yes at 0.304 ($5.00)
- 2026-11-08 coin_flip: Bitcoin Up or Down - November 9, 1:05AM-1:10AM ET -> Down at 0.517 ($5.00)
- 2026-11-08 sure_thing: Spread: Flames (-3.5) -> Flyers at 0.962 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Kuala Lumpur be 30°C on November 10? -> No at 0.971 ($5.00)
- 2026-11-08 sports_underdog: Spread: Fredrikstad FK (-1.5) -> Fredrikstad FK at 0.177 ($5.00)
- 2026-11-08 follow_move: Will the price of Ethereum be between $2,200 and $2,300 on November 14? -> No at 0.753 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Seoul (Incheon) be 4°C on November 10? -> No at 0.798 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (0 with a problem).
