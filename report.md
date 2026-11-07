# Polymarket strategy lab (pretend money)

Updated 2026-11-07 11:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 163 | 155/163 | +1.1% | +$8.77 | 2 | 236 | too early |
| 2 | sports_underdog | 241 | 56/241 | -9.3% | -$110.93 | 2 | 75 | too early |
| 3 | follow_move | 45 | 20/45 | -38.1% | -$85.65 | 2 | 100 | too early |
| 4 | fade_move | 60 | 18/60 | -39.3% | -$117.78 | 2 | 102 | too early |
| 5 | weather_forecast | 10 | 2/10 | -68.6% | -$34.32 | 1 | 163 | too early |
| 6 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 258 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 90 | 49/90 | +7.9% | +$35.14 | 2 | 310 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | weather_forecast | safe_no_week | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$5.34 | -$111.77 | -$10.37 | -$23.43 | -$34.32 | +$0.25 | +$27.71 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 |  | +$0.37 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Spread: Atalanta BC U23 (-2.5) -> Reggiana 1919 at 0.961 ($5.00)
- 2026-11-07 sports_underdog: Spread: IK Brage (-1.5) -> IK Brage at 0.229 ($5.00)
- 2026-11-07 follow_move: Will CZ post 20-39 posts from November 6 to November 13, 2026? -> Yes at 0.442 ($5.00)
- 2026-11-07 fade_move: Will OpenRouter process 205T or more tokens the week of November 2? -> No at 0.146 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Dallas be between 70-71°F on November 9? -> No at 0.723 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Denver be between 64-65°F on November 8? -> No at 0.924 ($5.00)
- 2026-11-07 coin_flip: Drogheda United FC leading at halftime? -> No at 0.642 ($5.00)
- 2026-11-07 sure_thing: Spread: Stevenage FC (-1.5) -> Oxford United FC at 0.924 ($5.00)
- 2026-11-07 sports_underdog: Will Qizilqum Zarafshon vs. Navbahor end in a draw? -> Yes at 0.259 ($5.00)
- 2026-11-07 follow_move: Will PPI YoY be 6.4% in October? -> Yes at 0.227 ($5.00)
- 2026-11-07 fade_move: Will Khamenei post 0-4 posts from November 6 to November 13, 2026? -> No at 0.270 ($5.00)
- 2026-11-07 weather_forecast: Will the highest temperature in Wuhan be 14°C on November 9? -> No at 0.681 ($5.00)

## Price gaps seen today

4 near-gaps recorded (full sets within a few cents of their payout). Cheapest: SBV Excelsior vs. Go Ahead Eagles - First Team to Score (yes), 1.005 for a $1 payout.

Runs in the last 24 hours: 36 (0 with a problem).
