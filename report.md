# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-11-03 12:07 UTC; 37 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): FAIL.** Decided on 2026-11-02, the 14th well-covered day: the pilot markets averaged -$12.01 a day on the cautious estimate, against the $1.50 needed. If only trades could fill paper orders (no fills from midpoint moves alone), it would have been -$1.89 a day. The verdict does not change after that day. For information, all 14 well-covered day(s) so far average -$12.01 (-$1.89 trades only).

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-03 (today, so far) | -$25.62 | -$21.68 | $2.53 | -$28.15 | -$9.49 | $34.91-$126.69 | 500 | -$168.72 |
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
| 2026-10-21 | -$16.58 | -$1.93 | $6.46 | -$23.04 | -$21.70 | $57.20-$181.31 | 452 | -$223.31 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$16.07, 36 watched markets (not thin), rewards $32.68-$156.75, trading -$126.02 (-$62.29 trades only), rebates $1.10, fills 844, 24h markouts -$225.50
- 1 tick(s) back: pilot cautious -$12.45, 36 watched markets (not thin), rewards $33.37-$196.23, trading -$85.58 (-$40.28 trades only), rebates $0.67, fills 818, 24h markouts -$166.28
- 2 tick(s) back: pilot cautious -$3.66, 36 watched markets (not thin), rewards $31.74-$217.13, trading -$55.39 (-$41.90 trades only), rebates $0.46, fills 712, 24h markouts -$139.94

Thin markets (10 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $142.94, paper trading -$57.52. They never count towards the go/no-go check.
