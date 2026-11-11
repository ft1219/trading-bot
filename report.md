# Polymarket strategy lab (pretend money)

Updated 2026-11-11 05:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 185 | 113/185 | +1.0% | +$8.86 | 6 | 150 | too early |
| 2 | sure_thing | 1231 | 1142/1231 | -0.5% | -$33.07 | 6 | 108 | too early |
| 3 | safe_no_week | 287 | 270/287 | -2.0% | -$28.73 | 6 | 321 | too early |
| 4 | sports_underdog | 974 | 222/974 | -15.2% | -$736.15 | 6 | 20 | too early |
| 5 | fade_move | 205 | 62/205 | -23.5% | -$240.86 | 6 | 167 | too early |
| 6 | weather_forecast | 268 | 134/268 | -25.4% | -$335.45 | 5 | 143 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1262 | 619/1262 | -6.0% | -$376.80 | 6 | 217 | yardstick |

What each one does:

- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | follow_move | sure_thing | safe_no_week | sports_underdog | fade_move | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-11 | -$1.33 | +$45.63 | -$2.15 | -$111.15 | +$8.47 | -$16.41 | -$40.05 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> No at 0.223 ($5.00)
- 2026-11-11 sure_thing: Will Ethereum dip to $1,950 on November 11? -> No at 0.953 ($5.00)
- 2026-11-11 safe_no_week: Will Pablo Picasso's “Le Baiser” sell for less than $40m at auction? -> No at 0.932 ($5.00)
- 2026-11-11 sports_underdog: Rainbow Six Siege: LOS vs Geekay Esports (BO3) - BLAST R6 Major Osaka Phase 2 - Swiss Stage -> LOS at 0.341 ($5.00)
- 2026-11-11 fade_move: Will NYC Mayor post 20-39 posts from November 10 to November 17, 2026? -> Yes at 0.818 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Cape Town be 17°C on November 12? -> No at 0.671 ($5.00)
- 2026-11-11 coin_flip: BNB Up or Down - November 11, 2:45AM-3:00AM ET -> Up at 0.527 ($5.00)
- 2026-11-11 follow_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> Yes at 0.351 ($5.00)
- 2026-11-11 sure_thing: South Carolina State Bulldogs vs. Notre Dame Fighting Irish -> Notre Dame Fighting Irish at 0.969 ($5.00)
- 2026-11-11 safe_no_week: Will Amedeo Modigliani's “Tête” sell for less than $28m at auction? -> No at 0.933 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: Spirit vs FUT Esports (BO3) - BLAST Rivals Group B -> FUT Esports at 0.177 ($5.00)
- 2026-11-11 fade_move: Will "Ebenezer" Opening Weekend Box Office be between 19m and 22m? -> No at 0.691 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
