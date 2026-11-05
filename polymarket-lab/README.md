# Polymarket strategy lab

Pretend trading only: public data, no account, no keys, no orders, no money.

The old practice mode (`polymarket-shadow/`) tested one idea, resting orders that earn liquidity rewards, and it failed its check (about -$12 a day). This lab tests several different ideas at the same time, on the same markets, and ranks them, so weak ideas can be dropped and new ones added while the good ones keep running.

## How a run works

Every 40 minutes, as its own job in the "Bots - every 40 minutes" workflow (`run.sh` -> `lab.py`):

1. Settles pretend positions whose markets have resolved: $1 a share for the winning side, $0 for the losing one (50 cents for a 50-50 result).
2. Lists every open event that ends within 7 days (about 7,500 events holding 100,000+ markets, most of them sports props).
3. Asks each strategy in `strategies.py` which markets it would buy. A strategy buys a given event at most once, and at most 8 new trades a run. A quote only counts when the gap between the best bid and the best ask is 5 cents or less: a lone 97-cent ask over a 1-cent bid is a dead market, not a near-certainty.
4. Fills each buy against the real order book: it walks up the asking prices, never above the strategy's price cap, until $5 is spent, and adds Polymarket's taker fee. If that buys fewer shares than Polymarket's smallest order (usually 5), there is no trade, because there could be no real one.
5. `weather_forecast`: for each daily temperature market ("Highest temperature in Paris on November 6?") whose station's local day has not started yet, works out the chance of each range from two free weather-model ensembles (ECMWF and GFS, 82 runs, via Open-Meteo) and buys a side only where that chance beats the price by 10 cents or more, both with the runs as they are and after allowing for model error. (The first version allowed for model error only, which on its own made every market favourite look overpriced; that was a constant, not a forecast.)
6. `price_gap`: in multi-choice events where exactly one choice wins, checks whether buying every "Yes" costs less than $1 a set (or every "No" less than n-1 dollars), using the real books for every choice, and buys whole sets of at least 5 shares if at least half a cent a set is left after fees (up to $20). Events Polymarket may still add choices to are skipped on the Yes side.
7. `report.py` rewrites `report.md` (made for reading on a phone) and `summary.json`.

Why buying at the asking price: a small trader can always take the asking price, so these pretend trades are close to what real ones would have been. Resting orders, which the old mode tested, depend on who trades against them, and paper trading cannot judge that well. What this lab cannot see: whether the price would move in the few seconds a real order takes, and price gaps that open and close between runs.

Pretend money is unlimited: every strategy takes every trade its rule allows. The dollar figures therefore show the size of the test, not what a 20-40 USDT account would make; compare strategies by their return per dollar.

## What the history said (Aug-Nov 2026)

Before the lab was built, about 180,000 finished markets and their hourly price history were replayed, buying "at the price" with a 1 cent gap and holding to the result. A second look (November 2026) corrected the first reading:

- Sports lines (moneyline, totals, spreads): prices were close to fair. Favourites at 90-98 cents gave about 0% a trade. The cheap sides looked great in the high-volume sample (+50% and more) but that was a data trap, since surprising games trade more volume; in the fair sample, cheap sides bought shortly before kick-off lost about 10-15% a trade. That is why `sports_underdog` is kept only as a check.
- Daily temperature markets: the first reading found +3% to +5% a trade for the 80-95 cent side bought two days out. That was an artifact: two days out these markets are hours old and nearly empty, and the midpoints of an event's eleven ranges added up to well over $1 (median 1.34). Where the books were coherent the same trade lost about 4%; with the midpoints scaled to add up to $1 it lost about 1%, in both the months used to look and the month held back. So there is no known edge in simply buying their favourites. `safe_no_week` still runs as the plain test of that, and `weather_forecast` is the one idea here with its own information source, with no history behind it either way.
- "Up or Down" crypto markets: 50-50 as priced, nothing to find.
- Everything else at 90-98 cents: roughly 0% to +1%, too few markets to be sure.

The replay covered only eight end-dates and used midpoints, not real asking prices. The lab's live numbers are the ones that count.

## The strategies

See `strategies.py` for the exact rules. Each has a start date. A rule is never changed in place once it has results: a changed idea gets a new name, so its results are not mixed with the old rule's. To stop one, set `"active": False`; its record stays in the report.

`coin_flip` is a yardstick: random sides of random markets. It should lose a little (price gap and fees). It is shown for comparison and takes no part in any verdict.

## The pass rule (fixed before any results)

A strategy is judged once, on the first run where all of this is true: it has been running for 14 days, it has at least 30 finished trades, and those trades finished on at least 10 different days (one lucky day is not evidence). That verdict is stored and never recomputed; judging again on every run would let a lucky streak show "PASS" at some point even with no edge at all.

It passes only if:

- it made money in total, and
- its number of wins is one that the prices alone would produce less than 1 time in 100. (A trade bought at 95 cents should win 95% of the time with no edge, so even 40 wins out of 40 at that price proves little; the same 40 wins at 80 cents would.)

`price_gap` is arithmetic, not a bet, so it passes on the total alone. A strategy that has made no trade at all after a month is marked "nothing to judge". Before judgment day the report says "too early", whatever the numbers look like.

Passing here does not put money in: that still needs the owner's explicit go, and the agreed pilot limits (20-40 USDT, $20 per market, $30 total loss cap in the first 3 months). The checks the lab makes are the ones a careful person would make; they are not a guarantee.

## Data

Everything goes to the `polymarket-lab-data` branch:

- `report.md`, `summary.json`: the current standing.
- `state.json`: open positions, which events each strategy already traded, stored verdicts, station coordinates.
- `trades/YYYY-MM.jsonl`, `settled/YYYY-MM.jsonl`: every pretend buy and every finished position, one file a month (so no file ever reaches GitHub's 100 MB limit).
- `runs.jsonl`: one line a run with its timing and any problems.
- `gaps/YYYY-MM-DD.jsonl`: each near price gap seen.
- `weather/YYYY-MM-DD.jsonl`: each forecast-versus-price disagreement found, trade or not.
- `forecasts/YYYY-MM-DD.jsonl`: one full forecast-versus-price snapshot per temperature event per day (every range's forecast chance, raw and smoothed, and its bid and ask), so that after a few weeks the forecasts can be checked against what happened and against the market.
- `forecasts_cache.json`: each station's latest ensemble, reused for 3 hours. Open-Meteo allows 600 weighted calls a minute and 10,000 a day on its free tier, and one ensemble call weighs about 16; the cache and a cap of 30 fresh calls a run keep the lab at about 400 calls a day.

The branch grows by a few MB a day. It is only ever cloned shallowly.

Weather data is from [Open-Meteo](https://open-meteo.com) (CC BY 4.0), whose free tier is for non-commercial use. This lab trades no money; if `weather_forecast` ever went live for real, that would need Open-Meteo's paid API or another source.

## If something breaks

A failed lab run turns the workflow run red and GitHub emails the owner; the forecasting jobs are separate and are not affected. Whatever the run managed to do is still saved, with the error in `runs.jsonl`, and the next run carries on. `report.md` shows the number of runs with a problem in the last 24 hours and the latest problem.

## Settings

Repository variable `POLYMARKET_LAB`: set it to `off` to pause the lab. Forecasting is not affected either way.

## Tests

```bash
cd polymarket-lab
python -m pytest -q tests
```
