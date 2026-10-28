# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-28 14:07 UTC; 37 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 8 of 14 well-covered days so far, averaging -$11.23 a day on the cautious estimate (-$0.69 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-28 (today, so far) | -$4.35 | $2.91 | $3.86 | -$8.20 | -$6.13 | $50.10-$223.63 | 560 | -$127.28 |
| 2026-10-27 | -$11.38 | $126.82 | $7.70 | -$19.09 | -$9.41 | $81.50-$479.58 | 710 | -$207.40 |
| 2026-10-26 | $2.04 | $27.32 | $11.03 | -$8.99 | -$0.72 | $37.06-$170.86 | 873 | -$187.94 |
| 2026-10-25 (partial day) | -$9.07 | $3.05 | $2.76 | -$11.62 | -$0.61 | $39.69-$194.47 | 841 | -$185.21 |
| 2026-10-24 (partial day) | -$16.09 | -$7.23 | $2.20 | -$18.10 | -$6.87 | $48.13-$206.89 | 605 | -$210.92 |
| 2026-10-23 | $2.49 | $14.41 | $6.86 | -$4.37 | -$5.83 | $80.86-$282.37 | 637 | -$136.13 |
| 2026-10-22 | $1.08 | $21.01 | $6.48 | -$5.40 | -$3.04 | $80.08-$382.40 | 496 | -$134.62 |
| 2026-10-21 | -$16.58 | -$1.93 | $6.46 | -$23.04 | -$21.70 | $57.20-$181.31 | 452 | -$223.31 |
| 2026-10-20 | -$21.61 | -$11.48 | $3.45 | -$24.90 | -$2.07 | $54.22-$198.26 | 577 | -$178.01 |
| 2026-10-19 | -$27.00 | -$24.31 | $0.43 | -$27.00 | -$1.49 | $31.25-$148.62 | 725 | -$268.04 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$20.84, 43 watched markets (not thin), rewards $67.51-$424.68, trading -$233.75 (-$125.46 trades only), rebates $0.30, fills 969, 24h markouts -$251.83
- 1 tick(s) back: pilot cautious -$11.38, 43 watched markets (not thin), rewards $81.50-$479.58, trading -$164.09 (-$96.15 trades only), rebates $0.23, fills 710, 24h markouts -$227.49
- 2 tick(s) back: pilot cautious -$10.51, 43 watched markets (not thin), rewards $81.02-$466.10, trading -$120.68 (-$55.15 trades only), rebates $0.21, fills 544, 24h markouts -$178.31

Thin markets (7 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $52.25, paper trading -$28.95. They never count towards the go/no-go check.
