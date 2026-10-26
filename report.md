# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-26 05:27 UTC; 36 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 6 of 14 well-covered days so far, averaging -$13.11 a day on the cautious estimate (-$2.21 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-26 (today, so far) | $2.29 | $9.63 | $3.29 | -$1.00 | -$0.33 | $12.99-$55.66 | 326 | -$75.09 |
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

- 0 tick(s) back: pilot cautious -$4.02, 40 watched markets (not thin), rewards $77.76-$284.37, trading -$152.15 (-$51.51 trades only), rebates $0.54, fills 1162, 24h markouts -$201.29
- 1 tick(s) back: pilot cautious $2.49, 40 watched markets (not thin), rewards $80.86-$282.37, trading -$102.09 (-$32.91 trades only), rebates $0.24, fills 637, 24h markouts -$127.78
- 2 tick(s) back: pilot cautious $1.93, 40 watched markets (not thin), rewards $85.07-$277.02, trading -$72.73 (-$27.73 trades only), rebates $0.15, fills 469, 24h markouts -$84.66

Thin markets (10 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $91.84, paper trading -$59.21. They never count towards the go/no-go check.
