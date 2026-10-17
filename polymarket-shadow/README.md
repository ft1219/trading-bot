# Polymarket practice mode

Paper market making on Polymarket's liquidity-reward markets, using only public data. No account, no keys, no orders, no money.

It answers one question before any money is risked: would a small bot that keeps a bid and an ask near the midpoint earn more in rewards and fee rebates than it loses when prices move against it?

## How a run works

Each run happens inside the 40-minute scheduled job (`run.sh`, called from `.github/workflows/metaculus-forecast.yaml`):

1. Once a UTC day, `selection.py` picks the watchlist from every market in the rewards program (`/sampling-markets` and `/rewards/markets/current`). It keeps markets that pay at least $10 a day, have a midpoint between 0.15 and 0.85, end more than 7 days away, are not live sports, and whose minimum reward size fits a $20 budget. It ranks them by the reward our orders would earn against the current book. The top two markets where other makers already quote near the middle become the pilot; a few "thin" markets are watched as well (see below).
2. `sim.py` replays every public trade record (the taker's and each maker's own leg) and every one-minute midpoint move since the last run against our paper orders at three distances from the midpoint (0, 1 and 2 ticks behind the closest prices). The fill rules are pessimistic: every share that traded at a price worse than ours fills our order first, up to its size; when the midpoint moves through our price, the rest of the order fills; quotes are based on the previous minute's midpoint and replaced only at the next one; and a $20 budget per market, where selling shares we already hold needs no cash.
3. `rewards.py` scores our paper orders the way Polymarket's sampler would see the live book with them in it, with the published formula, and records our share of the market's daily pool with competitors at their strongest and weakest possible. The run that picks the day's markets takes no reward sample, so the pilots are never credited with the moment they were chosen.
4. Paper holdings are valued at what selling them into the current book would fetch, level by level, after the taker fee. An hour and a day after each paper fill, it records how far the midpoint moved (markouts).
5. `report.py` rewrites `report.md` and `summary.json`.

## Data

Everything goes to the `polymarket-shadow-data` branch:

- `report.md`, `summary.json`: the daily table and the go/no-go check.
- `state.json`: watchlist, paper positions, and where each market's trade replay got to.
- `days/YYYY-MM-DD/`: `watchlist`, `samples` (reward share each run), `fills`, `markouts`, `closeouts` (positions sold when a market leaves the list), `gaps` (runs where a market's trade history was cut short) and `runs` (timing and errors), one JSON object per line.

## The go/no-go check (Gate A)

Fixed in the project plan before any data: after at least 14 days with good coverage (no gaps in a pilot market's trade history, and reward samples over at least half the day), the two pilot markets must average more than $1.50 a day on the cautious estimate of rewards + rebates + paper trading result. The cautious estimate assumes competitors are as strong as the book allows, that makers already inside the reward band would move up to our price, that a thin market pays nothing, and applies Polymarket's $1 minimum payout to each market separately. The pilot uses orders 1 tick behind the closest prices, also fixed in advance; the other two distances are shown for information only.

## Thin markets

The first live run found that most of the best-paying reward markets have almost nobody quoting near the middle: the gap between the best buy and sell prices is 20-60 cents, wider than the reward band. A paper order there looks like it collects the whole daily reward, because it is alone. In real life it would be the price, the "midpoint" it is placed around means little, and anyone who knows better would trade against it. Paper trading cannot measure that, so:

- a market is thin when, on either side, other makers have less than the minimum reward size inside the reward band;
- thin markets are never pilot markets, and in any run where a pilot market's book turns thin, the cautious estimate counts no reward for it;
- up to five thin markets are still watched, and the report shows their best-case numbers on a separate line, marked as not trustworthy.

## Known limits

- The public book adds up all makers at each price, so competitors' reward score is a range, not a number.
- Our paper orders are not in the real book, so nobody reacts to them. Assuming that makers in the band move up to our price is the cautious answer to that.
- The "size-cutoff-adjusted midpoint" is not defined in Polymarket's docs. We use the price where each side's depth first reaches the market's minimum reward size.
- Rewards are sampled every 40 minutes, not every minute as Polymarket does; fills use every trade and every one-minute midpoint.
- Rebates assume our share of a market's rebate pool equals our share of the fee-weighted maker volume, as the docs describe, and that the pool is the market's rebate rate times its taker fees.
- GitHub's runners are in the US, which Polymarket geoblocks for trading. Reading public data works; a real pilot must run from a Malaysian connection.

## Settings

Repository variables, all optional: `PM_BUDGET_PER_MARKET_USD` (default 20), `PM_WATCH_MARKETS` (25), `PM_PILOT_MARKETS` (2). Set `POLYMARKET_PRACTICE` to `off` to pause it.

## Tests

```bash
cd polymarket-shadow
python -m pytest -q tests
```

The tests use live API responses recorded on 2026-10-17 (`tests/fixtures/`).
