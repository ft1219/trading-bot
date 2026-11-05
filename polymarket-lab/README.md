# Polymarket strategy lab

Pretend trading only: public data, no account, no keys, no orders, no money.

The old practice mode (`polymarket-shadow/`) tested one idea, resting orders that earn liquidity rewards, and it failed its check (about -$12 a day). This lab tests several different ideas at the same time, on the same markets, and ranks them, so weak ideas can be dropped and new ones added while the good ones keep running.

## How a run works

Every 40 minutes, as its own job in the "Bots - every 40 minutes" workflow (`run.sh` -> `lab.py`):

1. Settles pretend positions whose markets have resolved: $1 a share for the winning side, $0 for the losing one (50 cents for a 50-50 result).
2. Lists every open market that ends within 7 days (about 6,000).
3. Asks each strategy in `strategies.py` which of them it would buy. A strategy buys a given event at most once, and at most 8 new trades a run.
4. Fills each buy against the real order book: it walks up the asking prices, never above the strategy's price cap, until $5 is spent, and adds Polymarket's taker fee. If less than $1 would fill, there is no trade.
5. `weather_forecast`: for each daily temperature market ("Highest temperature in Paris on November 6?"), works out the chance of each range from two free weather-model ensembles (ECMWF and GFS, 82 runs, via Open-Meteo, no key) and buys a side only where that chance beats the price by 10 cents or more, and only while the station's local day has not started yet (once it has, the market can see the real readings and the forecast is stale).
6. `price_gap`: in multi-choice events where exactly one choice wins, checks whether buying every "Yes" costs less than $1 a set (or every "No" less than n-1 dollars), using the real books for every choice, and buys the set if at least half a cent a set is left after fees (up to $20).
7. `report.py` rewrites `report.md` (made for reading on a phone) and `summary.json`.

Why buying at the asking price: a small trader can always take the asking price, so these pretend trades are close to what real ones would have been. Resting orders, which the old mode tested, depend on who trades against them, and paper trading cannot judge that well. What this lab cannot see: whether the price would move in the few seconds a real order takes, and price gaps that open and close between runs.

## What the history said (Aug-Nov 2026)

Before the lab was built, about 180,000 finished markets and their hourly price history were replayed (two samples: markets with $10k+ volume, and all markets on every fourth day). Buying "at the price" with a 1 cent gap, held to the result:

- Sports lines (moneyline, totals, spreads): prices were close to fair. Favourites at 90-98 cents gave about 0% a trade; the cheap sides looked great in the high-volume sample (+50% and more) but that was a data trap, since surprising games trade more volume, and the fair sample showed no edge.
- Daily temperature markets: the 80-95 cent side bought about two days before the end gave +3% to +5% a trade (n ≈ 360 in the months used to look, and it held up on the month kept back). That is why `safe_no_week`, `sure_thing` and `weather_forecast` exist.
- "Up or Down" crypto markets: 50-50 as priced, nothing to find.
- Everything else at 90-98 cents: roughly 0% to +1%, too few markets to be sure.

These replays use midpoints, not the real asking prices, so the lab's live numbers are the ones that count.

## The strategies

See `strategies.py` for the exact rules. Each has a start date. A rule is never changed in place: a changed idea gets a new name, so its results are not mixed with the old rule's. To stop one, set `"active": False`; its record stays in the report.

`coin_flip` is a yardstick: random sides of random markets. It should lose a little (price gap and fees). A real strategy must beat it.

## The pass rule (fixed before any results)

After 14 days and at least 30 finished trades, a strategy passes only if:

- it made money in total,
- its average return per trade minus two standard errors is still above zero (so it is unlikely to be luck), and
- it did better than `coin_flip`.

Before that the report says "too early", whatever the numbers look like. Passing here does not put money in: that still needs the owner's explicit go, and the agreed pilot limits (20-40 USDT, $20 per market, $30 total loss cap in the first 3 months).

## Data

Everything goes to the `polymarket-lab-data` branch: `report.md`, `summary.json`, `state.json` (open positions), `trades.jsonl`, `settled.jsonl`, `runs.jsonl`, `gaps/YYYY-MM-DD.jsonl` (each near price gap seen) and `weather/YYYY-MM-DD.jsonl` (each forecast-versus-price disagreement seen, trade or not).

## Settings

Repository variable `POLYMARKET_LAB`: set it to `off` to pause the lab. Forecasting is not affected either way.

## Tests

```bash
cd polymarket-lab
python -m pytest -q tests
```
