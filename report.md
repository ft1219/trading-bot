# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-23 00:47 UTC; 37 run(s) in the last 24 hours, 3 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 5 of 14 well-covered days so far, averaging -$16.66 a day on the cautious estimate (-$3.78 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-23 (today, so far) | -$0.97 | $1.86 | $0.02 | -$0.97 | -$0.01 | $1.78-$8.36 | 36 | -$2.37 |
| 2026-10-22 | $1.08 | $21.01 | $6.48 | -$5.40 | -$3.04 | $80.08-$382.40 | 496 | -$134.62 |
| 2026-10-21 | -$16.58 | -$1.93 | $6.46 | -$23.04 | -$21.70 | $57.20-$181.31 | 452 | -$223.31 |
| 2026-10-20 | -$21.61 | -$11.48 | $3.45 | -$24.90 | -$2.07 | $54.22-$198.26 | 577 | -$178.01 |
| 2026-10-19 | -$27.00 | -$24.31 | $0.43 | -$27.00 | -$1.49 | $31.25-$148.62 | 725 | -$268.04 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$5.50, 41 watched markets (not thin), rewards $69.61-$350.34, trading -$157.36 (-$77.61 trades only), rebates $0.77, fills 922, 24h markouts -$252.76
- 1 tick(s) back: pilot cautious $1.08, 41 watched markets (not thin), rewards $80.08-$382.40, trading -$104.31 (-$56.44 trades only), rebates $0.87, fills 496, 24h markouts -$214.54
- 2 tick(s) back: pilot cautious $7.22, 41 watched markets (not thin), rewards $71.15-$341.45, trading -$68.70 (-$53.22 trades only), rebates $0.34, fills 301, 24h markouts -$197.98

Thin markets (9 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $48.65, paper trading -$37.40. They never count towards the go/no-go check.
