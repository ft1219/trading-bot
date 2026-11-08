# Polymarket strategy lab (pretend money)

Updated 2026-11-08 05:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 443 | 416/443 | -0.4% | -$9.47 | 3 | 172 | too early |
| 2 | safe_no_week | 39 | 37/39 | -1.5% | -$2.89 | 3 | 276 | too early |
| 3 | sports_underdog | 460 | 106/460 | -11.4% | -$259.79 | 3 | 71 | too early |
| 4 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 116 | too early |
| 5 | weather_forecast | 57 | 25/57 | -33.3% | -$94.77 | 2 | 152 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 124 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 325 | 169/325 | +2.7% | +$44.08 | 3 | 291 | yardstick |

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
| 2026-11-08 | +$2.25 | -$4.16 | -$17.69 |  | +$12.50 | +$1.40 | -$16.27 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | +$2.49 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 | -$75.28 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: Club Universitario de Deportes vs. CD Moquegua: O/U 5.5 -> Under at 0.914 ($5.00)
- 2026-11-08 safe_no_week: Will Bhutan be in the top 3 at Eurovision Asia 2026? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Will Shandong Taishan FC vs. Chengdu Rongcheng FC end in a draw? -> Yes at 0.289 ($5.00)
- 2026-11-08 follow_move: Will South Korea be in the top 3 at Eurovision Asia 2026? -> No at 0.798 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Sao Paulo be 17°C on November 9? -> No at 0.671 ($5.00)
- 2026-11-08 fade_move: Will Bhutan be in the top 3 at Eurovision Asia 2026? -> Yes at 0.104 ($5.00)
- 2026-11-08 coin_flip: CD Universidad Catolica del Ecuador leading at halftime? -> No at 0.740 ($5.00)
- 2026-11-08 sure_thing: Spread: Arenas Club Getxo (-2.5) -> RC Deportivo Fabril at 0.933 ($5.00)
- 2026-11-08 safe_no_week: Will Wix (WIX) beat quarterly earnings? -> Yes at 0.943 ($5.00)
- 2026-11-08 sports_underdog: Spread: JEF United Ichihara Chiba (-1.5) -> JEF United Ichihara Chiba at 0.249 ($5.00)
- 2026-11-08 follow_move: Will Malaysia be the Jury Winner in the Eurovision Asia 2026 Grand Final? -> Yes at 0.691 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Karachi be 35°C on November 9? -> No at 0.642 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
