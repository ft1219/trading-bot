# Polymarket strategy lab (pretend money)

Updated 2026-11-06 11:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 5 | 5/5 | +5.4% | +$1.36 | 1 | 107 | too early |
| 2 | sports_underdog | 5 | 1/5 | -43.1% | -$10.76 | 1 | 40 | too early |
| 3 | follow_move | 1 | 0/1 | -100.0% | -$5.00 | 1 | 76 | too early |
| 4 | fade_move | 1 | 1/1 | +227.4% | +$11.37 | 1 | 85 | too early |
| 5 | safe_no_week | 0 | - | - | +$0.00 | 0 | 112 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 92 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 6 | 3/6 | -4.3% | -$1.29 | 1 | 106 | yardstick |

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

| Day | sure_thing | sports_underdog | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|
| 2026-11-06 | +$1.36 | -$10.76 | -$5.00 | +$11.37 | -$1.29 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sure_thing: WTI Crude Oil (WTI) closes above $88 on November 6? -> Yes at 0.904 ($5.00)
- 2026-11-06 sports_underdog: Spread: FC Goa (-1.5) -> FC Goa at 0.187 ($5.00)
- 2026-11-06 follow_move: Will Microsoft (MSFT) finish week of November 2 above $520? -> No at 0.245 ($5.00)
- 2026-11-06 fade_move: Will Microsoft (MSFT) finish week of November 2 above $520? -> Yes at 0.815 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Kuala Lumpur be 31°C on November 7? -> No at 0.963 ($5.00)
- 2026-11-06 weather_forecast: Will the highest temperature in London be 11°C on November 8? -> No at 0.671 ($5.00)
- 2026-11-06 coin_flip: Will 1. FC Köln vs. Bayer 04 Leverkusen end in a draw? -> No at 0.779 ($5.00)
- 2026-11-06 sure_thing: Wolfsberger AC leading at halftime? -> No at 0.914 ($5.00)
- 2026-11-06 sports_underdog: Will FC Goa vs. Bengaluru FC end in a draw? -> Yes at 0.290 ($5.00)
- 2026-11-06 follow_move: Will Quantum Computing (QUBT) beat quarterly earnings? -> Yes at 0.730 ($5.00)
- 2026-11-06 fade_move: XRP Up or Down on November 6? -> Up at 0.117 ($5.00)
- 2026-11-06 safe_no_week: Will annual inflation be 3.8% in October? -> No at 0.941 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 14 (0 with a problem).
