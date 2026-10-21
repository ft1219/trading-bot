# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-21 14:07 UTC; 37 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 3 of 14 well-covered days so far, averaging -$21.55 a day on the cautious estimate (-$3.16 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-21 (today, so far) | -$18.93 | -$11.29 | $3.33 | -$21.60 | -$15.66 | $39.98-$126.54 | 324 | -$164.10 |
| 2026-10-20 | -$21.61 | -$11.48 | $3.45 | -$24.90 | -$2.07 | $54.22-$198.26 | 577 | -$178.01 |
| 2026-10-19 | -$27.00 | -$24.31 | $0.43 | -$27.00 | -$1.49 | $31.25-$148.62 | 725 | -$268.04 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$22.28, 43 watched markets (not thin), rewards $48.17-$177.89, trading -$219.85 (-$65.48 trades only), rebates $2.53, fills 754, 24h markouts -$287.74
- 1 tick(s) back: pilot cautious -$21.61, 43 watched markets (not thin), rewards $54.22-$198.26, trading -$167.08 (-$52.99 trades only), rebates $2.29, fills 577, 24h markouts -$255.67
- 2 tick(s) back: pilot cautious -$22.32, 43 watched markets (not thin), rewards $62.82-$203.81, trading -$135.61 (-$39.08 trades only), rebates $1.87, fills 542, 24h markouts -$205.59

Thin markets (6 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $6.82, paper trading -$12.40. They never count towards the go/no-go check.
