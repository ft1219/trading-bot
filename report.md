# Polymarket strategy lab (pretend money)

Updated 2026-11-06 16:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 11 | 11/11 | +5.6% | +$3.08 | 1 | 157 | too early |
| 2 | sports_underdog | 24 | 6/24 | -21.7% | -$25.30 | 1 | 67 | too early |
| 3 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 160 | too early |
| 4 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 109 | too early |
| 5 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 122 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 113 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 8 | 4/8 | -4.5% | -$1.81 | 1 | 160 | yardstick |

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
| 2026-11-06 | +$3.08 | -$25.30 | +$0.12 | -$5.00 | +$11.37 | -$1.81 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Spread: FK Kudrivka (-2.5) -> FK Chornomorets Odesa at 0.962 ($5.00)
- 2026-11-06 sports_underdog: Will TOP Oss win on 2026-11-06? -> Yes at 0.259 ($5.00)
- 2026-11-06 safe_no_week: Will "ArcheAge Chronicles" be the #1 Steam Weekly Top Seller for the week of November 3 - November 10, 2026? -> No at 0.983 ($5.00)
- 2026-11-06 follow_move: Will CZ post 40-59 posts from November 3 to November 10, 2026? -> Yes at 0.482 ($5.00)
- 2026-11-06 fade_move: Will CZ post 40-59 posts from November 3 to November 10, 2026? -> No at 0.562 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Wuhan be 12°C on November 8? -> Yes at 0.164 ($3.62)
- 2026-11-06 coin_flip: Spread: Browns (-2.5) -> Browns at 0.377 ($5.00)
- 2026-11-06 sure_thing: FC Hradec Králové vs. SK Sigma Olomouc: Neither team to score first? -> No at 0.971 ($5.00)
- 2026-11-06 sports_underdog: Will USL Dunkerque win on 2026-11-06? -> Yes at 0.341 ($5.00)
- 2026-11-06 safe_no_week: Will the lowest temperature in Guangzhou be 21°C on November 8? -> No at 0.981 ($5.00)
- 2026-11-06 follow_move: Will "The One About Matthew Perry: Season 1" be the #2 US Netflix show this week? -> Yes at 0.422 ($5.00)
- 2026-11-06 fade_move: Will Gintautas Kindurys win the 2026 Northern Nalšia district by-election? -> No at 0.420 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 21 (0 with a problem).
