# Polymarket strategy lab (pretend money)

Updated 2026-11-06 12:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sports_underdog | 6 | 1/6 | -46.7% | -$12.47 | 1 | 46 | too early |
| 2 | sure_thing | 5 | 5/5 | +5.4% | +$1.36 | 1 | 115 | too early |
| 3 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 81 | too early |
| 4 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 92 | too early |
| 5 | safe_no_week | 0 | - | - | +$0.00 | 0 | 120 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 94 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 6 | 3/6 | -4.3% | -$1.29 | 1 | 114 | yardstick |

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
| 2026-11-06 | -$12.47 | +$1.36 | -$5.00 | +$11.37 | -$1.29 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sports_underdog: Will FC Gomel vs. FK Arsenal Dzerzhinsk end in a draw? -> Yes at 0.259 ($5.00)
- 2026-11-06 sure_thing: Exact Score: FC Eindhoven 0 - 1 Jong Ajax Amsterdam? -> No at 0.964 ($5.00)
- 2026-11-06 follow_move: Will Meta Platforms, Inc. (META) hit (LOW) $580 Week of November 2 2026? -> Yes at 0.278 ($5.00)
- 2026-11-06 fade_move: Will Meta Platforms, Inc. (META) hit (LOW) $580 Week of November 2 2026? -> No at 0.855 ($5.00)
- 2026-11-06 safe_no_week: Will there be 7 earthquakes of 5.5 or above magnitude worldwide? -> No at 0.933 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Amsterdam be 7°C on November 7? -> No at 0.572 ($5.00)
- 2026-11-06 coin_flip: CA Unión vs. CA Vélez Sarsfield: CA Unión O/U 0.5 -> Over at 0.771 ($5.00)
- 2026-11-06 sports_underdog: Spread: FC Lokomotiv 1929 Sofia (-1.5) -> FC Lokomotiv 1929 Sofia at 0.218 ($5.00)
- 2026-11-06 sure_thing: Call of Duty: FaZe Vegas vs Huntsmen (BO5) - Monster Launch Invitational Group B -> FaZe Vegas at 0.924 ($5.00)
- 2026-11-06 follow_move: Will Coinbase Global, Inc. (COIN) hit (LOW) $130 Week of November 2 2026? -> Yes at 0.288 ($5.00)
- 2026-11-06 fade_move: Will Coinbase Global, Inc. (COIN) hit (LOW) $130 Week of November 2 2026? -> No at 0.787 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Chengdu be 20°C on November 8? -> No at 0.943 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 15 (0 with a problem).
