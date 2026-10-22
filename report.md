# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-22 16:47 UTC; 37 run(s) in the last 24 hours, 1 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 4 of 14 well-covered days so far, averaging -$20.34 a day on the cautious estimate (-$5.36 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-22 (today, so far) | -$1.12 | $14.20 | $4.73 | -$5.85 | -$2.29 | $62.86-$305.95 | 405 | -$131.41 |
| 2026-10-21 | -$16.58 | -$1.93 | $6.46 | -$23.04 | -$21.70 | $57.20-$181.31 | 452 | -$223.31 |
| 2026-10-20 | -$21.61 | -$11.48 | $3.45 | -$24.90 | -$2.07 | $54.22-$198.26 | 577 | -$178.01 |
| 2026-10-19 | -$27.00 | -$24.31 | $0.43 | -$27.00 | -$1.49 | $31.25-$148.62 | 725 | -$268.04 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$31.47, 41 watched markets (not thin), rewards $50.32-$199.68, trading -$225.32 (-$79.89 trades only), rebates $0.47, fills 502, 24h markouts -$226.18
- 1 tick(s) back: pilot cautious -$16.58, 41 watched markets (not thin), rewards $57.20-$181.31, trading -$178.78 (-$53.46 trades only), rebates $0.50, fills 452, 24h markouts -$162.36
- 2 tick(s) back: pilot cautious -$17.05, 41 watched markets (not thin), rewards $45.67-$149.47, trading -$170.56 (-$50.62 trades only), rebates $0.21, fills 453, 24h markouts -$130.42

Thin markets (9 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $45.53, paper trading -$49.25. They never count towards the go/no-go check.
