# Polymarket practice mode

Paper trading only: no money, no account. Last updated 2026-10-19 18:07 UTC; 36 run(s) in the last 24 hours, 11 with problems noted in `runs.jsonl`.

**Go/no-go check (Gate A): NOT ENOUGH DATA YET.** 1 of 14 well-covered days so far, averaging -$18.31 a day on the cautious estimate (-$5.70 if only trades could fill paper orders). The verdict is taken once, on the 14th, and needs more than $1.50 a day.

Pilot: the top 2 markets each day where others already quote near the middle, $20 each, orders 1 tick(s) behind the closest prices to the midpoint.

| Day | Pilot cautious | Pilot optimistic | Pilot rewards (low) | Pilot trading | Pilot trading (trades only) | Watched markets (not thin), rewards low-high | Fills | 1h markouts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-19 (today, so far) | -$21.40 | -$18.71 | $0.43 | -$21.40 | $1.01 | $24.43-$107.73 | 624 | -$254.64 |
| 2026-10-18 | -$27.92 | -$20.14 | $3.27 | -$30.99 | -$17.54 | $34.08-$133.19 | 622 | -$260.29 |
| 2026-10-17 (partial day) | -$11.78 | -$4.99 | $0.92 | -$11.78 | $0.00 | $14.11-$56.36 | 233 | -$67.75 |

Other distances from the midpoint, latest full day:

- 0 tick(s) back: pilot cautious -$29.35, 35 watched markets (not thin), rewards $30.21-$128.48, trading -$184.97 (-$74.62 trades only), rebates $1.70, fills 983, 24h markouts -$104.83
- 1 tick(s) back: pilot cautious -$27.92, 35 watched markets (not thin), rewards $34.08-$133.19, trading -$172.74 (-$56.78 trades only), rebates $1.34, fills 622, 24h markouts -$68.55
- 2 tick(s) back: pilot cautious -$8.22, 35 watched markets (not thin), rewards $35.95-$139.53, trading -$127.85 (-$39.09 trades only), rebates $1.12, fills 638, 24h markouts -$48.88

Thin markets (11 watched): nobody else quotes near the middle, so a paper order there would set the price alone and these numbers cannot be trusted. Best case rewards $90.93, paper trading -$69.88. They never count towards the go/no-go check.
