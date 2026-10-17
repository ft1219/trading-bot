"""
Read-only access to Polymarket's public APIs. Standard library only, so the
scheduled job needs no install step.

Nothing here signs requests, holds keys or places orders.

Response shapes were checked against live responses on 2026-10-17 (see
tests/fixtures/), including:
- CLOB books list bids lowest-first and asks highest-first, prices and sizes
  as strings.
- /prices-history points are {"t": unix seconds, "p": midpoint}, about one a
  minute with fidelity=1.
- data-api /trades with the default takerOnly=true returns one record per
  taker fill: "side" is the taker's side on "asset", "price" is in dollars.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Iterable

CLOB = "https://clob.polymarket.com"
DATA = "https://data-api.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
USER_AGENT = "trading-bot-shadow/0.1 (read-only)"
TRADES_PAGE = 500
# data-api refuses offsets past a few thousand; at 40-minute polling even the
# busiest market we track trades far fewer than this between runs.
TRADES_MAX_OFFSET = 3000


class ApiError(RuntimeError):
    pass


Fetch = Callable[[str, Any], Any]


def http_json(url: str, body: Any = None, timeout: float = 20, tries: int = 3) -> Any:
    """GET (or POST when body is given) and decode JSON, retrying briefly."""
    data = None
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    last: Exception | None = None
    for attempt in range(tries):
        request = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            last = e
            if e.code not in (429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise ApiError(f"{url}: {last!r}")


def _paged_clob(path: str, fetch: Fetch, max_pages: int = 100) -> list[dict]:
    items: list[dict] = []
    cursor = ""
    for _ in range(max_pages):
        url = f"{CLOB}{path}" + (f"?next_cursor={urllib.parse.quote(cursor)}" if cursor else "")
        page = fetch(url, None)
        if not isinstance(page, dict) or not isinstance(page.get("data"), list):
            raise ApiError(f"{path}: unexpected page shape")
        items.extend(page["data"])
        cursor = page.get("next_cursor") or ""
        if not cursor or cursor == "LTE=":
            return items
    raise ApiError(f"{path}: more than {max_pages} pages")


def sampling_markets(fetch: Fetch = http_json) -> list[dict]:
    """Every market currently in the liquidity-rewards program."""
    return _paged_clob("/sampling-markets", fetch)


def current_reward_configs(fetch: Fetch = http_json) -> dict[str, dict]:
    """condition_id -> {"total_daily_rate", "rewards_min_size", "rewards_max_spread", ...}."""
    return {m["condition_id"]: m for m in _paged_clob("/rewards/markets/current", fetch)}


def gamma_markets(condition_ids: Iterable[str], fetch: Fetch = http_json, chunk: int = 20) -> dict[str, dict]:
    """conditionId -> gamma market (fee schedule, holding rewards, dates)."""
    ids = list(condition_ids)
    out: dict[str, dict] = {}
    for i in range(0, len(ids), chunk):
        query = "&".join(f"condition_ids={c}" for c in ids[i:i + chunk])
        rows = fetch(f"{GAMMA}/markets?limit={chunk}&{query}", None)
        for row in rows if isinstance(rows, list) else []:
            if row.get("conditionId"):
                out[row["conditionId"]] = row
    return out


def books(token_ids: Iterable[str], fetch: Fetch = http_json, chunk: int = 40) -> dict[str, dict]:
    """token_id -> order book, fetched in batches."""
    ids = list(token_ids)
    out: dict[str, dict] = {}
    for i in range(0, len(ids), chunk):
        rows = fetch(f"{CLOB}/books", [{"token_id": t} for t in ids[i:i + chunk]])
        if not isinstance(rows, list):
            raise ApiError("/books: unexpected shape")
        for row in rows:
            out[str(row.get("asset_id"))] = row
    return out


def price_history(token_id: str, start_ts: int, end_ts: int, fetch: Fetch = http_json) -> list[tuple[int, float]]:
    """[(unix seconds, midpoint)] at about one point a minute, oldest first."""
    url = f"{CLOB}/prices-history?market={token_id}&startTs={int(start_ts)}&endTs={int(end_ts)}&fidelity=1"
    body = fetch(url, None)
    points = body.get("history") if isinstance(body, dict) else None
    if not isinstance(points, list):
        raise ApiError("/prices-history: unexpected shape")
    return sorted((int(p["t"]), float(p["p"])) for p in points)


def taker_trades_since(condition_id: str, since_ts: int, fetch: Fetch = http_json) -> tuple[list[dict], bool]:
    """
    Taker fills in a market newer than since_ts, oldest first.
    Returns (trades, complete); complete is False when the page limit cut the
    history short, so the caller can mark that window as partial.
    """
    found: list[dict] = []
    offset = 0
    while offset <= TRADES_MAX_OFFSET:
        url = f"{DATA}/trades?market={condition_id}&limit={TRADES_PAGE}&offset={offset}"
        page = fetch(url, None)
        if not isinstance(page, list):
            raise ApiError("/trades: unexpected shape")
        for t in page:
            if int(t["timestamp"]) > since_ts:
                found.append(t)
        if len(page) < TRADES_PAGE or int(page[-1]["timestamp"]) <= since_ts:
            found.sort(key=lambda t: (int(t["timestamp"]), t.get("transactionHash", "")))
            return found, True
        offset += TRADES_PAGE
    found.sort(key=lambda t: (int(t["timestamp"]), t.get("transactionHash", "")))
    return found, False


def parallel(calls: dict[str, Callable[[], Any]], workers: int = 8) -> dict[str, Any]:
    """Run independent calls at once; a failed call's value is its exception."""
    results: dict[str, Any] = {}
    with cf.ThreadPoolExecutor(workers) as pool:
        futures = {key: pool.submit(fn) for key, fn in calls.items()}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:  # recorded per market, never fatal for the run
                results[key] = e
    return results
