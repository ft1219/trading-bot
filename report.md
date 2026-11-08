# Polymarket strategy lab (pretend money)

Updated 2026-11-08 15:27 UTC. Each pretend trade is $5, bought at the real asking price plus fees, held to the result. Pretend money is unlimited, so the dollar columns show the size of the test, not what a small real account would make; compare strategies by "Per $1".

## Scoreboard (finished trades only)

| # | Strategy | Finished | Won | Per $1 | Profit | Days | Open | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | sure_thing | 498 | 468/498 | -0.3% | -$7.83 | 3 | 237 | too early |
| 2 | safe_no_week | 55 | 52/55 | -1.8% | -$5.06 | 3 | 300 | too early |
| 3 | sports_underdog | 564 | 126/564 | -15.3% | -$429.47 | 3 | 84 | too early |
| 4 | weather_forecast | 84 | 42/84 | -21.7% | -$89.89 | 2 | 177 | too early |
| 5 | follow_move | 60 | 31/60 | -24.3% | -$72.78 | 2 | 124 | too early |
| 6 | fade_move | 76 | 23/76 | -43.6% | -$165.84 | 3 | 135 | too early |
| 7 | price_gap | 0 | - | - | +$0.00 | 0 | 0 | too early |
| 8 | coin_flip | 423 | 212/423 | -2.9% | -$60.98 | 3 | 313 | yardstick |

What each one does:

- **sure_thing**: Buy the almost-sure side (90-97c) in the last 24 hours (sports and other markets).
- **safe_no_week**: Buy the almost-sure side (92-98.5c), 1-7 days before the end, no sports.
- **sports_underdog**: Buy the cheap side (15-35c) of sports games in the 3 hours before kick-off (history says this loses; kept as a check).
- **weather_forecast**: Daily temperature markets, before the day starts: buy No on a range when 82 weather-model runs give it 10c+ less chance than the market (or Yes when they give it 10c+ more), with and without allowing for model error; in practice nearly always No against the market favourite.
- **follow_move**: After a traded 10c+ move in a day, buy the side that went up.
- **fade_move**: After a traded 10c+ move in a day, buy the side that went down.
- **price_gap**: Multi-choice markets whose prices add up to less than $1: buy every choice.
- **coin_flip**: Yardstick: random side, random market (should lose a little).

Pass rule (fixed in advance): a strategy is judged once, on the first run after 14 days with at least 30 finished trades on at least 10 different days. It passes only if it made money AND its number of wins is one that the prices alone would produce less than 1 time in 100 (so it is unlikely to be luck). The verdict is then kept, not recomputed. Before that, "too early"; "nothing to judge" means no trade at all after a month. "Days" counts the different days on which its trades finished.

## Profit by day (trades that finished that day)

| Day | sure_thing | safe_no_week | sports_underdog | weather_forecast | follow_move | fade_move | coin_flip |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | +$3.88 | -$6.32 | -$187.36 | +$17.38 |  | +$1.40 | -$121.34 |
| 2026-11-07 | -$25.83 | +$0.90 | -$242.94 | -$107.27 | +$2.49 | -$72.89 | +$52.92 |
| 2026-11-06 | +$14.11 | +$0.37 | +$0.84 |  | -$75.28 | -$94.35 | +$7.43 |

## Latest pretend buys (newest of each strategy first)

- 2026-11-08 sure_thing: OFI Crete vs. Atromitos Athinon: Neither team to score first? -> No at 0.943 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Dallas be between 78-79°F on November 10? -> No at 0.952 ($5.00)
- 2026-11-08 sports_underdog: Spread: SK Sturm Graz (-1.5) -> SK Sturm Graz at 0.198 ($5.00)
- 2026-11-08 weather_forecast: Will the lowest temperature in Seoul (Incheon) be 4°C on November 10? -> No at 0.798 ($5.00)
- 2026-11-08 follow_move: Will the White House call a full lid by 6:30 PM on November 9? -> No at 0.460 ($5.00)
- 2026-11-08 fade_move: Will Clooless win Best Content Group at the 2026 Streamer Awards? -> Yes at 0.146 ($5.00)
- 2026-11-08 coin_flip: Hyperliquid Up or Down - November 8, 11:15PM-11:30PM ET -> Up at 0.527 ($5.00)
- 2026-11-08 sure_thing: Spread: MVV Maastricht (-1.5) -> FC Emmen at 0.952 ($5.00)
- 2026-11-08 safe_no_week: Will the highest temperature in Milan be 10°C on November 10? -> No at 0.985 ($5.00)
- 2026-11-08 sports_underdog: Spread: KFC Komárno (-1.5) -> KFC Komárno at 0.341 ($5.00)
- 2026-11-08 weather_forecast: Will the highest temperature in Shanghai be 16°C on November 10? -> No at 0.642 ($5.00)
- 2026-11-08 follow_move: Will CoreWeave say "Revenue" 20+ times during earnings call? -> Yes at 0.699 ($5.00)

## Price gaps seen today

No near-gaps today.

Runs in the last 24 hours: 37 (0 with a problem).
