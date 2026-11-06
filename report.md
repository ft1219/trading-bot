# Polymarket strategy lab (pretend money)

Updated 2026-11-06 07:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 3 | 3/3 | +3.3% | +$0.50 | 1 | 61 | too early |
| 2 | sports_underdog | 3 | 1/3 | -5.1% | -$0.76 | 1 | 13 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 64 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 62 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 64 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 64 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 2 | 2/2 | +91.4% | +$9.14 | 1 | 62 | yardstick |

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

| Day | sure_thing | sports_underdog | coin_flip |
|---|---|---|---|
| 2026-11-06 | +$0.50 | -$0.76 | +$9.14 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Spread: Antalyaspor (-1.5) -> Bursaspor at 0.952 ($5.00)
- 2026-11-06 sports_underdog: Dota 2: Xipto Esports vs Froglings (BO3) - DreamLeague Division 2 Group A -> Xipto Esports at 0.361 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Busan be 12°C on November 7? -> No at 0.962 ($5.00)
- 2026-11-06 follow_move: Will the price of XRP be above $1.20 on November 9? -> No at 0.645 ($5.00)
- 2026-11-06 fade_move: Will Natus Vincere Win the IEM Beijing 2026? -> Yes at 0.209 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Wuhan be 15°C on November 8? -> No at 0.642 ($5.00)
- 2026-11-06 coin_flip: Will Gaziantep FK vs. Kasımpaşa SK end in a draw? -> Yes at 0.300 ($5.00)
- 2026-11-06 sure_thing: Exact Score: FK Septemvri Sofia 0 - 0 FC Lokomotiv 1929 Sofia? -> No at 0.943 ($5.00)
- 2026-11-06 sports_underdog: Dota 2: potn9ki vs Zenith (BO3) - DreamLeague Division 2 Group A -> Zenith at 0.321 ($5.00)
- 2026-11-06 safe_no_week: Will the price of XRP be above $1.10 on November 8? -> Yes at 0.955 ($5.00)
- 2026-11-06 follow_move: Will the price of XRP be above $1.20 on November 7? -> No at 0.682 ($5.00)
- 2026-11-06 fade_move: Will Gold (XAUUSD) hit (HIGH) $4,150 Week of November 2 2026? -> Yes at 0.124 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 8 (0 with a problem).
