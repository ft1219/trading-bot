# Polymarket strategy lab (pretend money)

Updated 2026-11-06 23:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 83 | 81/83 | +3.4% | +$14.11 | 1 | 173 | too early |
| 2 | sports_underdog | 108 | 29/108 | +0.2% | +$0.84 | 1 | 71 | too early |
| 3 | fade_move | 50 | 16/50 | -37.7% | -$94.35 | 1 | 102 | too early |
| 4 | follow_move | 39 | 17/39 | -38.7% | -$75.28 | 1 | 98 | too early |
| 5 | safe_no_week | 2 | 2/2 | +3.7% | +$0.37 | 1 | 208 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 133 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 43 | 22/43 | +3.5% | +$7.43 | 1 | 213 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | fade_move | follow_move | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|
| 2026-11-06 | +$14.11 | +$0.84 | -$94.35 | -$75.28 | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Exact Score: Portsmouth FC 0 - 0 Stoke City FC? -> No at 0.914 ($5.00)
- 2026-11-06 sports_underdog: Spread: South Florida (-14.5) -> South Florida at 0.164 ($5.00)
- 2026-11-06 fade_move: Ethereum Up or Down on November 7? -> Down at 0.386 ($5.00)
- 2026-11-06 follow_move: Will "Thriller - Michael Jackson" be the Billboard Hot 100 #2 song for the week of November 14? -> Yes at 0.156 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Houston be between 62-63°F on November 8? -> No at 0.925 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Qingdao be 6°C on November 8? -> No at 0.769 ($5.00)
- 2026-11-06 coin_flip: Will Paksi FC vs. Zalaegerszeg TE end in a draw? -> Yes at 0.249 ($5.00)
- 2026-11-06 sure_thing: Spread: Ljungskile SK (-2.5) -> Landskrona BoIS at 0.962 ($5.00)
- 2026-11-06 sports_underdog: Spread: CA Banfield (-1.5) -> CA Banfield at 0.177 ($5.00)
- 2026-11-06 fade_move: Will Pixelworks (PXLW) beat quarterly earnings? -> Yes at 0.239 ($5.00)
- 2026-11-06 follow_move: Will Pixelworks (PXLW) beat quarterly earnings? -> No at 0.800 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Istanbul be 9°C on November 8? -> No at 0.975 ($5.00)

## Price gaps seen today

2 near-gaps recorded (full sets within a few cents of their payout). Cheapest: NZ Election: Labour Party # of seats? (yes), 1.002 for a $1 payout.

Runs in the last 24 hours: 32 (0 with a problem).
