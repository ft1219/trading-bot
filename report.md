# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-31 08:47 UTC; 36 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 11 of 14 well-covered days so far, averaging -$11.76 a day on the cautious estimate (-$1.02 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-31 (today, so far) | -$19.00 | -$15.13 | $1.62 | -$20.03 | -$12.03 | $20.79-$162.23 | 253 | -$109.79 |
| 2026-10-30 | -$16.28 | -$10.63 | $2.09 | -$17.75 | -$6.35 | $75.69-$398.10 | 685 | -$229.49 |
| 2026-10-29 | -$21.66 | $14.00 | $7.82 | -$28.95 | -$9.21 | $50.02-$303.90 | 752 | -$235.91 |
| 2026-10-28 | -$2.59 | $6.94 | $6.01 | -$8.60 | -$5.43 | $76.38-$357.13 | 769 | -$198.77 |
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

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$17.70, 42 watched markets (not thin), rewards $68.93-$381.54, trading -$244.40 (-$141.34 trades only), rebates $0.32, fills 1133, 24h markouts -$240.11
- 1 tick(s) back: pilot cautious -$16.28, 42 watched markets (not thin), rewards $75.69-$398.10, trading -$209.76 (-$125.75 trades only), rebates $0.33, fills 685, 24h markouts -$227.78
- 2 tick(s) back: pilot cautious -$15.47, 42 watched markets (not thin), rewards $69.85-$406.07, trading -$178.62 (-$118.77 trades only), rebates $0.17, fills 576, 24h markouts -$149.29

Thin markets (6 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $21.93, paper trading -$15.35. They never count towards the go/no-go check.
