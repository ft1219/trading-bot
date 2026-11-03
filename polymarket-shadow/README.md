# Polymarket practice mode

Paper market making on Polymarket's liquidity-reward markets, using only public data. No account, no keys, no orders, no money.

It answers one question before any money is risked: would a small bot that keeps a bid and an ask near the midpoint earn more in rewards and fee rebates than it loses when prices move against it?

**Answer: no.** It failed its go/no-go check on 2 November 2026: over 14 well-covered days the two pilot markets averaged -$12.01 a day on the cautious estimate (-$1.89 with trades only), against more than $1.50 needed. It was switched off on 3 November 2026. The code, tests and the `polymarket-shadow-data` branch are kept for reference; running it again means adding its step back to `.github/workflows/metaculus-forecast.yaml` (see that file's history).

## How a run works

Each run happened inside the 40-minute scheduled job (`run.sh`, called from `.github/workflows/metaculus-forecast.yaml` until 3 November 2026):

1. Once a UTC day, `selection.py` picks the watchlist from every market in the rewards program (`/sampling-markets` and `/rewards/markets/current`). It keeps markets that pay at least $10 a day, have a midpoint between 0.15 and 0.85, end more than 7 days away, are not live sports, and whose minimum reward size fits a $20 budget. It ranks them by the reward our orders would earn against the current book. The top two markets where other makers already quote near the middle become the pilot; "thin" markets fill the remaining watch slots, at least five of them (see below).
2. `sim.py` replays every public trade record (the taker's and each maker's own leg) and every one-minute midpoint move since the last run against our paper orders at three distances from the midpoint (0, 1 and 2 ticks behind the closest prices). The fill rules are pessimistic: every share that traded at a price worse than ours fills our order first, up to its size; when the midpoint moves through our price, the rest of the order fills; quotes are based on the previous minute's midpoint and replaced only at the next one; and a $20 budget per market, where selling shares we already hold needs no cash and money lost on round trips leaves the budget until rewards and rebates make it up (each day's are counted as paid the next day, and only if they reach the $1 minimum payout). If the price history has a hole of more than 10 minutes, the last quotes are assumed to have stayed up through it, and the stretch is marked as a gap. A second replay of the same quotes lets only trades fill them, for comparison (see Known limits).
3. `rewards.py` scores our paper orders the way Polymarket's sampler would see the live book with them in it, with the published formula, and records our share of the market's daily pool with competitors at their strongest and weakest possible. Each sample stands for the time since the previous one (at most 90 minutes). A run where a market has no usable book records a sample that earns nothing. The run that picks the day's markets takes no reward sample, so the pilots are never credited with the moment they were chosen.
4. A market that resolves is settled at $1 or $0 a share and leaves the list. Paper holdings are valued at what selling them into the current book would fetch, level by level, after the taker fee. An hour and a day after each paper fill, it records how far the midpoint moved (markouts).
5. `report.py` rewrites `report.md` and `summary.json`.

## Data

Everything goes to the `polymarket-shadow-data` branch:

- `report.md`, `summary.json`: the daily table and the go/no-go check.
- `state.json`: watchlist, paper positions, and where each market's trade replay got to.
- `days/YYYY-MM-DD/`: `watchlist`, `samples` (reward share each run), `fills`, `markouts`, `closeouts` (positions sold or settled when a market leaves the list or changes role), `gaps` (stretches of a market's trades or midpoint history that could not be replayed, filed under every day they touch) and `runs` (timing and errors), one JSON object per line.

## The go/no-go check (Gate A)

Fixed in the project plan before any data: after at least 14 days with good coverage (no gaps in a pilot market's history, and reward samples over at least half the day), the two pilot markets must average more than $1.50 a day on the cautious estimate of rewards + rebates + paper trading result. The cautious estimate assumes competitors are as strong as the book allows, that makers already inside the reward band would move up to our price, that a thin market or time without a sample pays nothing, and applies Polymarket's $1 minimum payout to each market separately. Rewards and rebates are averaged over the well-covered days; the paper trading result is averaged over every day since the first pilot, so losses on a badly covered day still count. The verdict is taken once, on the day the 14th well-covered day is reached, and does not change after that: checking a running average every day until it passes would let a losing strategy through far more often. The running average is still shown, for information. If the pilot settings differ from the plan (2 markets, $20 each, 1 tick back), the check gives no verdict. The pilot uses orders 1 tick behind the closest prices, also fixed in advance; the other two distances are shown for information only.

## Thin markets

The first live run found that most of the best-paying reward markets have almost nobody quoting near the middle: the gap between the best buy and sell prices is 20-60 cents, wider than the reward band. A paper order there looks like it collects the whole daily reward, because it is alone. In real life it would be the price, the "midpoint" it is placed around means little, and anyone who knows better would trade against it. Paper trading cannot measure that, so:

- a market is thin when, on either side, other makers have less than the minimum reward size inside the reward band;
- thin markets are never pilot markets, and in any run where a pilot market's book turns thin, the cautious estimate counts no reward for it;
- at least five thin markets are still watched, and more when fewer established markets qualify (thin ones fill the rest of the 25 slots, never the pilot slots); the report shows their best-case numbers on a separate line, marked as not trustworthy.

## Known limits

- The public book adds up all makers at each price, so competitors' reward score is a range, not a number.
- Our paper orders are not in the real book, so nobody reacts to them. Assuming that makers in the band move up to our price is the cautious answer to that.
- The "size-cutoff-adjusted midpoint" is not defined in Polymarket's docs. We use the price where each side's depth first reaches the market's minimum reward size.
- The public data has trades and one-minute midpoints, not every order. When the midpoint moves through our price with no trade, a real order may or may not have been hit: in jumpy books the midpoint also moves when makers cancel and re-post. The check assumes it was hit; the report also shows a "trades only" result that assumes it was not. The truth is likely in between.
- Rewards are sampled every 40 minutes, not every minute as Polymarket does; fills use every trade and every one-minute midpoint.
- Rebates assume our share of a market's rebate pool equals our share of the fee-weighted maker volume, as the docs describe, and that the pool is the market's rebate rate times its taker fees.
- GitHub's runners are in the US, which Polymarket geoblocks for trading. Reading public data works; a real pilot must run from a Malaysian connection.

## Settings

Repository variables, all optional: `PM_WATCH_MARKETS` (default 25). The pilot's size and count (2 markets, $20 each) are fixed by the plan, so they are not variables.

The top of `report.md` says when it was last updated and how many runs in the last 24 hours noted a problem.

## Tests

```bash
cd polymarket-shadow
python -m pytest -q tests
```

The tests use live API responses recorded on 2026-10-17 (`tests/fixtures/`).
