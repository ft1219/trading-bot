# Polymarket strategy lab (pretend money)

Updated 2026-11-11 11:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | follow_move | 187 | 114/187 | +0.6% | +$5.99 | 6 | 157 | too early |
| 2 | sure_thing | 1263 | 1174/1263 | -0.4% | -$22.95 | 6 | 118 | too early |
| 3 | safe_no_week | 306 | 288/306 | -1.9% | -$28.65 | 6 | 334 | too early |
| 4 | sports_underdog | 989 | 226/989 | -14.8% | -$729.65 | 6 | 24 | too early |
| 5 | fade_move | 209 | 63/209 | -24.2% | -$252.41 | 6 | 171 | too early |
| 6 | weather_forecast | 289 | 145/289 | -25.1% | -$357.00 | 5 | 159 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 1 | too early |
| 8 | coin_flip | 1318 | 650/1318 | -5.6% | -$364.79 | 6 | 233 | yardstick |

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
| 2026-11-11 | -$4.19 | +$55.75 | -$2.08 | -$104.65 | -$3.09 | -$37.96 | -$28.04 |
| 2026-11-10 | +$55.84 | -$15.92 | -$2.64 | +$61.94 | +$1.13 | -$101.16 | -$214.60 |
| 2026-11-09 | +$11.06 | +$1.64 | -$5.28 | -$181.99 | -$67.00 | -$76.41 | +$26.49 |
| 2026-11-08 | +$16.06 | -$52.70 | -$19.92 | -$262.85 | -$16.21 | -$34.20 | -$209.00 |
| 2026-11-07 | +$2.49 | -$25.83 | +$0.90 | -$242.94 | -$72.89 | -$107.27 | +$52.92 |
| 2026-11-06 | -$75.28 | +$14.11 | +$0.37 | +$0.84 | -$94.35 |  | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-11 follow_move: Will "How to Rob a Bank" Opening Weekend Box Office be less than 7m? -> Yes at 0.602 ($5.00)
- 2026-11-11 sure_thing: SPY (SPY) Up or Down on November 11? -> Up at 0.923 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Wuhan be 12°C on November 13? -> No at 0.952 ($5.00)
- 2026-11-11 sports_underdog: BNP Paribas Nordic Open: Taylor Fritz vs Cameron Norrie -> Cameron Norrie at 0.270 ($5.00)
- 2026-11-11 fade_move: Will "How to Rob a Bank" Opening Weekend Box Office be less than 7m? -> No at 0.472 ($5.00)
- 2026-11-11 weather_forecast: Will the highest temperature in Istanbul be 22°C on November 13? -> No at 0.769 ($5.00)
- 2026-11-11 price_gap: All Yes on: Japan GDP growth in Q3 2026 (QoQ Annualized)? at 0.995 ($15.92)
- 2026-11-11 coin_flip: Bitcoin Up or Down - November 11, 11:30PM-11:35PM ET -> Down at 0.517 ($5.00)
- 2026-11-11 follow_move: Will Dani win the GMGN GGC Season 1 Grand Final? -> Yes at 0.493 ($5.00)
- 2026-11-11 sure_thing: Solana Up or Down on November 11? -> Up at 0.916 ($5.00)
- 2026-11-11 safe_no_week: Will the highest temperature in Houston be between 72-73°F on November 13? -> No at 0.962 ($5.00)
- 2026-11-11 sports_underdog: Dota 2: HULIGANI vs PuckChamp (BO3) - DreamLeague Division 2 Group B -> PuckChamp at 0.177 ($5.00)

## Price gaps seen today

5 near-gaps recorded (full sets within a few cents of their payout). Cheapest: Japan GDP growth in Q3 2026 (QoQ Annualized)? (yes), 0.994 for a $1 payout.

Runs in the last 24 hours: 37 (37 with a problem).
Latest problem: 37 position(s) still open more than 3 days after their market ended
