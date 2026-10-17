import urllib.parse

import pytest

import pmapi

CID = "0xf85c8a7a66365d0c58ec863a48bc65fb40e5071514a36c2931bc665c02f3cd7b"


def query(url):
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))


class Pages:
    """Serves a list of /v2/trades rows (newest first) in pages linked by cursor."""

    def __init__(self, rows, size, has_more_without_cursor=False):
        self.rows, self.size, self.calls = rows, size, []
        self.has_more_without_cursor = has_more_without_cursor

    def __call__(self, url, body):
        q = query(url)
        self.calls.append(q)
        start = int(q.get("cursor", 0))
        page = self.rows[start:start + self.size]
        more = start + self.size < len(self.rows)
        cursor = None if (not more or self.has_more_without_cursor) else str(start + self.size)
        return {"data": page, "pagination": {"has_more": more, "limit": self.size, "offset": start, "next_cursor": cursor}}


def test_recorded_page_comes_back_oldest_first(fx):
    page = fx("trades_v2_page")
    since = min(r["timestamp"] for r in page["data"]) - 1
    found, complete = pmapi.trades_since(CID, since, lambda url, body: page)
    assert complete
    assert len(found) == len(page["data"])
    assert [r["timestamp"] for r in found] == sorted(r["timestamp"] for r in page["data"])
    assert {"token_id", "transaction_hash", "side", "price", "size"} <= set(found[0])


def test_asks_for_every_party_and_resends_filters_with_the_cursor():
    rows = [{"timestamp": 1000 - i, "transaction_hash": f"0x{i}"} for i in range(25)]
    fetch = Pages(rows, size=10)
    found, complete = pmapi.trades_since(CID, 0, fetch)
    assert complete and len(found) == 25
    assert len(fetch.calls) == 3
    for q in fetch.calls:
        assert q["condition"] == CID and q["taker_only"] == "false"
    assert "cursor" not in fetch.calls[0] and fetch.calls[1]["cursor"] == "10"


def test_stops_at_the_first_page_older_than_since():
    rows = [{"timestamp": 1000 - i, "transaction_hash": f"0x{i}"} for i in range(25)]
    fetch = Pages(rows, size=10)
    found, complete = pmapi.trades_since(CID, 995, fetch)
    assert complete and [r["timestamp"] for r in found] == [996, 997, 998, 999, 1000]
    assert len(fetch.calls) == 1


def test_page_limit_marks_the_history_as_cut_short(monkeypatch):
    monkeypatch.setattr(pmapi, "TRADES_MAX_PAGES", 2)
    rows = [{"timestamp": 1000 - i, "transaction_hash": f"0x{i}"} for i in range(25)]
    found, complete = pmapi.trades_since(CID, 0, Pages(rows, size=10))
    assert not complete and len(found) == 20


def test_more_pages_without_a_cursor_is_cut_short():
    rows = [{"timestamp": 1000 - i, "transaction_hash": f"0x{i}"} for i in range(25)]
    found, complete = pmapi.trades_since(CID, 0, Pages(rows, size=10, has_more_without_cursor=True))
    assert not complete and len(found) == 10


def test_unexpected_shape_raises():
    with pytest.raises(pmapi.ApiError):
        pmapi.trades_since(CID, 0, lambda url, body: [])
