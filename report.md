# Polymarket strategy lab (pretend money)

Updated 2026-11-10 06:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 1020 | 943/1020 | -1.3% | -$67.07 | 5 | 109 | too early |
| 2 | safe_no_week | 202 | 190/202 | -2.0% | -$20.35 | 5 | 312 | too early |
| 3 | follow_move | 136 | 83/136 | -2.1% | -$13.99 | 5 | 136 | too early |
| 4 | sports_underdog | 851 | 193/851 | -15.1% | -$637.31 | 5 | 22 | too early |
| 5 | weather_forecast | 206 | 99/206 | -27.6% | -$281.02 | 4 | 138 | too early |
| 6 | fade_move | 155 | 45/155 | -33.5% | -$259.61 | 5 | 146 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 1012 | 498/1012 | -5.7% | -$288.30 | 5 | 195 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | follow_move | sports_underdog | weather_forecast | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | -$4.29 | +$3.58 | +$31.68 | +$49.63 | -$63.14 | -$9.16 | -$166.15 |
| 2026-11-09 | +$1.64 | -$5.28 | +$11.06 | -$181.99 | -$76.41 | -$67.00 | +$26.49 |
| 2026-11-08 | -$52.70 | -$19.92 | +$16.06 | -$262.85 | -$34.20 | -$16.21 | -$209.00 |
| 2026-11-07 | -$25.83 | +$0.90 | +$2.49 | -$242.94 | -$107.27 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | -$75.28 | +$0.84 |  | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-10 sure_thing: Bitcoin Up or Down - November 10, 1AM ET -> Down at 0.963 ($5.00)
- 2026-11-10 safe_no_week: Will the highest temperature in Seoul (Incheon) be 18°C on November 12? -> No at 0.981 ($5.00)
- 2026-11-10 follow_move: Will Bitcoin dip to $72,000 November 9-15? -> No at 0.607 ($5.00)
- 2026-11-10 sports_underdog: Hersonissos 3: Felix Gill vs Menelaos Efstathiou -> Menelaos Efstathiou at 0.187 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Seoul (Incheon) be 16°C on November 12? -> No at 0.612 ($5.00)
- 2026-11-10 fade_move: Will Bitcoin dip to $72,000 November 9-15? -> Yes at 0.437 ($5.00)
- 2026-11-10 coin_flip: Club Atletico La Paz leading at halftime? -> Yes at 0.226 ($5.00)
- 2026-11-10 sure_thing: Clippers vs. Suns: O/U 206.5 -> Over at 0.905 ($5.00)
- 2026-11-10 safe_no_week: Will Man I Need (Olivia Dean) be nominated for Record of the Year at the 69th Annual GRAMMY Awards? -> Yes at 0.962 ($5.00)
- 2026-11-10 follow_move: Will Kai Cenat finish his GTA marathon by November 11, 2:59 PM ET? -> Yes at 0.701 ($5.00)
- 2026-11-10 sports_underdog: Brisbane 3: Hiroki Moriya vs Alex Bolt -> Hiroki Moriya at 0.310 ($5.00)
- 2026-11-10 weather_forecast: Will the highest temperature in Tokyo be 18°C on November 12? -> No at 0.652 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 36 (23 with a problem).
Latest problem: 6 position(s) still open more than 3 days after their market ended
