# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-11-04 06:07 UTC; 36 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): FAIL.** Decided on 2026-11-02, the 14th well-covered day: the pilot markets averaged -$12.01 a day on the cautious estimate, against the $1.50 needed. If only trades could fill paper orders (no fills from midpoint moves alone), it would have been -$1.89 a day. The verdict does not change after that day. For information, all 15 well-covered day(s) so far average -$12.71 (-$2.17 trades only).

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-04 (today, so far) | -$6.08 | $3.74 | $2.25 | -$7.39 | -$1.50 | $20.18-$120.97 | 152 | -$92.06 |
| 2026-11-03 | -$24.55 | -$15.58 | $4.67 | -$29.22 | -$11.53 | $63.39-$271.83 | 725 | -$210.31 |
| 2026-11-02 | -$12.45 | $13.59 | $3.38 | -$14.94 | -$10.74 | $33.37-$196.23 | 818 | -$121.23 |
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

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$24.82, 38 watched markets (not thin), rewards $79.14-$327.17, trading -$175.01 (-$74.73 trades only), rebates $3.31, fills 827, 24h markouts -$183.09
- 1 tick(s) back: pilot cautious -$24.55, 38 watched markets (not thin), rewards $63.39-$271.83, trading -$131.59 (-$60.95 trades only), rebates $3.38, fills 725, 24h markouts -$126.11
- 2 tick(s) back: pilot cautious -$23.99, 38 watched markets (not thin), rewards $50.65-$227.57, trading -$126.46 (-$48.50 trades only), rebates $2.33, fills 594, 24h markouts -$100.10

Thin markets (11 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $132.60, paper trading -$56.83. They never count towards the go/no-go check.
