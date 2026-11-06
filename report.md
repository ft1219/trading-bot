# Polymarket strategy lab (pretend money)

Updated 2026-11-06 17:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | fade_move | 12 | 8/12 | +42.2% | +$25.30 | 1 | 120 | too early |
| 2 | sure_thing | 14 | 14/14 | +5.7% | +$3.99 | 1 | 170 | too early |
| 3 | sports_underdog | 35 | 9/35 | -9.2% | -$15.73 | 1 | 72 | too early |
| 4 | follow_move | 11 | 3/11 | -60.3% | -$33.17 | 1 | 107 | too early |
| 5 | safe_no_week | 1 | 1/1 | +2.3% | +$0.12 | 1 | 172 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 118 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 8 | 4/8 | -4.5% | -$1.81 | 1 | 176 | yardstick |

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
| 2026-11-06 | +$25.30 | +$3.99 | -$15.73 | -$33.17 | +$0.12 | -$1.81 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 fade_move: Will Elon Musk post 40-64 tweets from November 7 to November 9, 2026? -> Yes at 0.259 ($5.00)
- 2026-11-06 sure_thing: Exact Score: Chelsea FC 1 - 0 Everton FC? -> No at 0.952 ($5.00)
- 2026-11-06 sports_underdog: Will Hamburger SV vs. Borussia Mönchengladbach end in a draw? -> Yes at 0.290 ($5.00)
- 2026-11-06 follow_move: Will White House post 200+ posts from November 6 to November 13, 2026? -> No at 0.432 ($5.00)
- 2026-11-06 safe_no_week: Will Elon Musk post 140-159 tweets from November 6 to November 13, 2026? -> No at 0.982 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Sao Paulo be 19°C on November 8? -> No at 0.730 ($5.00)
- 2026-11-06 coin_flip: Will Grenoble Foot 38 win on 2026-11-06? -> Yes at 0.229 ($5.00)
- 2026-11-06 fade_move: Will there be 0 earthquakes of 6.5 or above magnitude worldwide? -> No at 0.310 ($5.00)
- 2026-11-06 sure_thing: Will IK Start win on 2026-11-07? -> No at 0.933 ($5.00)
- 2026-11-06 sports_underdog: Dota 2: iLTW TEAM vs LenS Team (BO3) - Media Eleague Group Stage -> iLTW TEAM at 0.239 ($5.00)
- 2026-11-06 follow_move: Will Elon Musk post 40-64 tweets from November 7 to November 9, 2026? -> No at 0.789 ($5.00)
- 2026-11-06 safe_no_week: Will CZ post 80-99 posts from November 6 to November 13, 2026? -> No at 0.933 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 23 (0 with a problem).
