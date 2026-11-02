# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-11-02 15:27 UTC; 36 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 13 of 14 well-covered days so far, averaging -$11.95 a day on the cautious estimate (-$1.46 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-02 (today, so far) | -$15.94 | -$4.80 | $2.59 | -$17.73 | -$13.53 | $23.41-$139.95 | 588 | -$107.57 |
| 2026-11-01 | -$9.94 | $13.59 | $3.06 | -$13.00 | -$2.80 | $48.77-$246.54 | 763 | -$192.64 |
| 2026-10-31 | -$15.57 | -$8.09 | $3.84 | -$18.81 | -$11.41 | $36.90-$374.72 | 625 | -$177.53 |
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

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$19.03, 39 watched markets (not thin), rewards $36.12-$209.04, trading -$193.20 (-$101.33 trades only), rebates $1.45, fills 832, 24h markouts -$218.09
- 1 tick(s) back: pilot cautious -$9.94, 39 watched markets (not thin), rewards $48.77-$246.54, trading -$165.21 (-$90.50 trades only), rebates $1.78, fills 763, 24h markouts -$169.07
- 2 tick(s) back: pilot cautious -$9.27, 39 watched markets (not thin), rewards $48.87-$316.56, trading -$123.34 (-$67.34 trades only), rebates $1.45, fills 637, 24h markouts -$142.78

Thin markets (8 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $29.26, paper trading -$22.76. They never count towards the go/no-go check.
