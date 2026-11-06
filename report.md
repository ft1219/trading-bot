# Polymarket strategy lab (pretend money)

Updated 2026-11-06 09:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 3 | 3/3 | +3.3% | +$0.50 | 1 | 85 | too early |
| 2 | sports_underdog | 3 | 1/3 | -5.1% | -$0.76 | 1 | 27 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 88 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 72 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 77 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 86 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 4 | 2/4 | -4.3% | -$0.86 | 1 | 84 | yardstick |

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
| 2026-11-06 | +$0.50 | -$0.76 | -$0.86 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: Hyperliquid Up or Down - November 6, 4:15AM-4:30AM ET -> Up at 0.898 ($5.00)
- 2026-11-06 sports_underdog: Spread: Maccabi Tel Aviv FC (-1.5) -> Maccabi Petah Tikva FC at 0.351 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Amsterdam be 5°C on November 7? -> No at 0.975 ($5.00)
- 2026-11-06 follow_move: Will Apple (AAPL) finish week of November 2 above $345? -> No at 0.718 ($5.00)
- 2026-11-06 fade_move: Will the price of XRP be above $1.20 on November 9? -> Yes at 0.528 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in Manila be 34°C on November 8? -> No at 0.847 ($5.00)
- 2026-11-06 coin_flip: Solana Up or Down - November 7, 12:30AM-12:35AM ET -> Up at 0.527 ($5.00)
- 2026-11-06 sure_thing: Spread: US Amal Tiznit (-1.5) -> Union Touarga Sports at 0.952 ($5.00)
- 2026-11-06 sports_underdog: Will Lamphun Warriors FC vs. Sukhothai FC end in a draw? -> Yes at 0.229 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Austin be between 66-67°F on November 7? -> No at 0.952 ($5.00)
- 2026-11-06 follow_move: Will the price of XRP be between $1.20 and $1.30 on November 8? -> Yes at 0.487 ($5.00)
- 2026-11-06 fade_move: Will the price of Bitcoin be between $80,000 and $82,000 on November 10? -> Yes at 0.106 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 11 (0 with a problem).
