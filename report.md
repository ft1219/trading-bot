# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-30 01:27 UTC; 36 run(s) in the last 24 hours, 22 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 10 of 14 well-covered days so far, averaging -$11.32 a day on the cautious estimate (-$0.64 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-30 (today, so far) | -$11.65 | -$11.65 | $0.00 | -$11.65 | -$13.80 | $5.75-$15.99 | 93 | -$38.01 |
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
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$25.34, 41 watched markets (not thin), rewards $42.17-$270.92, trading -$213.01 (-$110.39 trades only), rebates $0.00, fills 968, 24h markouts -$231.96
- 1 tick(s) back: pilot cautious -$21.66, 41 watched markets (not thin), rewards $50.02-$303.90, trading -$191.05 (-$106.76 trades only), rebates $0.00, fills 752, 24h markouts -$143.02
- 2 tick(s) back: pilot cautious -$13.87, 41 watched markets (not thin), rewards $52.31-$318.78, trading -$150.03 (-$71.35 trades only), rebates $0.00, fills 721, 24h markouts -$136.24

Thin markets (9 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $44.38, paper trading -$49.15. They never count towards the go/no-go check.
