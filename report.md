# Polymarket strategy lab (pretend money)

Updated 2026-11-11 02:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 185 | 113/185 | +1.0% | +$8.86 | 6 | 147 | too early |
| 2 | sure_thing | 1192 | 1104/1192 | -1.2% | -$73.73 | 6 | 112 | too early |
| 3 | safe_no_week | 283 | 267/283 | -1.7% | -$24.43 | 6 | 321 | too early |
| 4 | sports_underdog | 946 | 217/946 | -14.3% | -$674.14 | 6 | 46 | too early |
| 5 | fade_move | 205 | 62/205 | -23.5% | -$240.86 | 6 | 160 | too early |
| 6 | weather_forecast | 263 | 131/263 | -25.6% | -$331.62 | 5 | 148 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1213 | 595/1213 | -5.8% | -$352.91 | 6 | 226 | yardstick |

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
| 2026-11-11 | -$1.33 | +$4.97 | +$2.15 | -$49.14 | +$8.47 | -$12.57 | -$16.16 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will "Ghost Soldier" score at least 20 on the Rotten Tomatoes Tomatometer? -> Yes at 0.856 ($5.00)
- 2026-11-11 sure_thing: Exact Score: Piratas Veracruz 0 - 0 Club Atletico La Paz? -> No at 0.962 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Panama City be 31°C on November 12? -> No at 0.967 ($5.00)
- 2026-11-11 sports_underdog: Counter-Strike: Vitality vs Team Falcons (BO3) - BLAST Rivals Group A -> Team Falcons at 0.321 ($5.00)
- 2026-11-11 fade_move: Will Geese be nominated for Best New Artist at the 69th Annual GRAMMY Awards? -> No at 0.177 ($5.00)
- 2026-11-11 weather_forecast: Will the lowest temperature in Cape Town be 17°C on November 12? -> No at 0.671 ($5.00)
- 2026-11-11 coin_flip: XRP Up or Down - November 11, 4:30PM-4:45PM ET -> Down at 0.527 ($5.00)
- 2026-11-11 follow_move: Will Don't Be Dumb (A$AP Rocky) be nominated for Best Rap Album at the 69th Annual GRAMMY Awards? -> Yes at 0.827 ($5.00)
- 2026-11-11 sure_thing: Portland State Vikings vs. Colorado State Rams -> Colorado State Rams at 0.933 ($5.00)
- 2026-11-11 safe_no_week: Will MrBeast's next video get between 35 and 40 million views on day 1? -> No at 0.924 ($5.00)
- 2026-11-11 sports_underdog: Thunder vs. Trail Blazers: O/U 217.5 -> Under at 0.338 ($5.00)
- 2026-11-11 fade_move: Will WORSHIP (ASAKE) be nominated for Best Dance Pop Recording at the 69th Annual GRAMMY Awards? -> Yes at 0.104 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (36 with a problem).
Latest problem: 8 position(s) still open more than 3 days after their market ended
