# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-20 10:07 UTC; 36 run(s) in the last 24 hours, 0 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 2 of 14 well-covered days so far, averaging -$21.72 a day on the cautious estimate (-$4.81 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-20 (today, so far) | -$15.70 | -$6.58 | $2.90 | -$18.44 | -$2.12 | $22.94-$93.95 | 465 | -$164.08 |
| 2026-10-19 | -$27.00 | -$24.31 | $0.43 | -$27.00 | -$1.49 | $31.25-$148.62 | 725 | -$268.04 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$26.66, 40 watched markets (not thin), rewards $21.20-$109.77, trading -$238.23 (-$28.93 trades only), rebates $0.97, fills 774, 24h markouts -$221.19
- 1 tick(s) back: pilot cautious -$27.00, 40 watched markets (not thin), rewards $31.25-$148.62, trading -$202.60 (-$29.35 trades only), rebates $0.91, fills 725, 24h markouts -$215.14
- 2 tick(s) back: pilot cautious -$25.20, 40 watched markets (not thin), rewards $29.15-$134.71, trading -$158.12 (-$17.85 trades only), rebates $0.91, fills 702, 24h markouts -$181.61

Thin markets (9 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $28.14, paper trading -$58.10. They never count towards the go/no-go check.
