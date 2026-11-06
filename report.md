# Polymarket strategy lab (pretend money)

Updated 2026-11-06 10:47 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sports_underdog | 5 | 1/5 | -43.1% | -$10.76 | 1 | 34 | too early |
| 2 | sure_thing | 4 | 4/4 | +5.3% | +$1.07 | 1 | 100 | too early |
| 3 | safe_no_week | 0 | - | - | +$0.00 | 0 | 104 | too early |
| 4 | follow_move | 0 | - | - | +$0.00 | 0 | 76 | too early |
| 5 | fade_move | 0 | - | - | +$0.00 | 0 | 85 | too early |
| 6 | weather_forecast | 0 | - | - | +$0.00 | 0 | 91 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 5 | 3/5 | +14.9% | +$3.71 | 1 | 99 | yardstick |

What each one does:

- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sports_underdog | sure_thing | coin_flip |
|---|---|---|---|
| 2026-11-06 | -$10.76 | +$1.07 | +$3.71 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-06 sports_underdog: Spread: PFC Sogdiana (-1.5) -> PFC Sogdiana at 0.218 ($5.00)
- 2026-11-06 sure_thing: Will Tesla (TSLA) close at <$375 on the final day of trading of the week of Nov 2 – Nov 6? -> Yes at 0.962 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Seoul (Incheon) be 6°C on November 8? -> No at 0.962 ($5.00)
- 2026-11-06 follow_move: Will Quantum Computing (QUBT) beat quarterly earnings? -> Yes at 0.730 ($5.00)
- 2026-11-06 fade_move: XRP Up or Down on November 6? -> Up at 0.117 ($5.00)
- 2026-11-06 weather_forecast: Will the lowest temperature in Wuhan be 13°C on November 7? -> No at 0.681 ($5.00)
- 2026-11-06 coin_flip: Will FC Viktoria Cologne vs. 1. FC Saarbrucken end in a draw? -> Yes at 0.239 ($5.00)
- 2026-11-06 sports_underdog: Will PFC Sogdiana vs. PFK Dinamo Samarqand end in a draw? -> Yes at 0.270 ($5.00)
- 2026-11-06 sure_thing: Exact Score: FC Goa 0 - 0 Bengaluru FC? -> No at 0.933 ($5.00)
- 2026-11-06 safe_no_week: Will the highest temperature in Tel Aviv be 19°C on November 7? -> No at 0.968 ($5.00)
- 2026-11-06 follow_move: Will the price of Solana be above $95 on November 10? -> No at 0.830 ($5.00)
- 2026-11-06 fade_move: Will Tesla (TSLA) close at <$375 on the final day of trading of the week of Nov 2 – Nov 6? -> No at 0.104 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 13 (0 with a problem).
