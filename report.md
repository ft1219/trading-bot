# Polymarket strategy lab (pretend money)

Updated 2026-11-07 06:07 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 131 | 124/131 | +0.6% | +$3.68 | 2 | 204 | too early |
| 2 | sports_underdog | 181 | 39/181 | -13.8% | -$123.93 | 2 | 75 | too early |
| 3 | follow_move | 44 | 20/44 | -36.7% | -$80.65 | 2 | 96 | too early |
| 4 | fade_move | 59 | 18/59 | -38.2% | -$112.78 | 2 | 99 | too early |
| 5 | safe_no_week | 3 | 3/3 | +4.1% | +$0.62 | 2 | 220 | too early |
| 6 | weather_forecast | 1 | 0/1 | -100.0% | -$5.00 | 1 | 142 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 68 | 34/68 | +3.1% | +$10.30 | 2 | 268 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | sports_underdog | follow_move | fade_move | safe_no_week | weather_forecast | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | -$10.43 | -$124.77 | -$5.37 | -$18.43 | +$0.25 | -$5.00 | +$2.87 |
| 2026-11-06 | +$14.11 | +$0.84 | -$75.28 | -$94.35 | +$0.37 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-07 sure_thing: Helsingborgs IF vs. Falkenbergs FF: Neither team to score first? -> No at 0.971 ($5.00)
- 2026-11-07 sports_underdog: Will Melbourne City FC vs. Western Sydney Wanderers FC end in a draw? -> Yes at 0.270 ($5.00)
- 2026-11-07 follow_move: Will UK GDP growth in Q3 2026 be between 0.6% and 0.7%? -> Yes at 0.575 ($5.00)
- 2026-11-07 fade_move: Will the price of Ethereum be above $2,100 on November 12? -> No at 0.158 ($5.00)
- 2026-11-07 safe_no_week: Will ChatGPT be #2 Free App in the US Apple App Store on November 13? -> No at 0.981 ($5.00)
- 2026-11-07 weather_forecast: Will the lowest temperature in Busan be 6°C or higher on November 8? -> Yes at 0.128 ($3.58)
- 2026-11-07 coin_flip: FCI Levadia Tallinn leading at halftime? -> Yes at 0.452 ($5.00)
- 2026-11-07 sure_thing: Exact Score: Drogheda United FC 0 - 0 University College Dublin? -> No at 0.954 ($5.00)
- 2026-11-07 sports_underdog: Spread: Gimcheon Sangmu FC (-1.5) -> Gimcheon Sangmu FC at 0.198 ($5.00)
- 2026-11-07 follow_move: Dogecoin Up or Down on November 7? -> Down at 0.792 ($5.00)
- 2026-11-07 fade_move: Will CZ post 0-19 posts from November 6 to November 13, 2026? -> Yes at 0.130 ($5.00)
- 2026-11-07 safe_no_week: Will the highest temperature in Panama City be 29°C on November 8? -> No at 0.980 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
