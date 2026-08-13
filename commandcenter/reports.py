"""commandcenter.reports — daily revenue reporting utilities."""

from __future__ import annotations
from datetime import datetime
from typing import List, Dict, Any


def business_day(timestamp_iso: str) -> str:
    """
    Convert an ISO‑8601 UTC timestamp (e.g. ``2026-08-12T02:10:00Z``) to the UTC calendar day
    ``YYYY‑MM‑DD`` string.

    The function treats the input as UTC regardless of the local server timezone.
    """
    # The timestamps in the test suite always end with a literal ``Z`` indicating UTC.
    dt = datetime.strptime(timestamp_iso, "%Y-%m-%dT%H:%M:%SZ")
    return dt.date().isoformat()


def daily_revenue(orders: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Aggregate order amounts by the UTC business day.

    ``orders`` is a list of dicts each containing:
        - ``ts``: an ISO‑8601 UTC timestamp string
        - ``amount_cents``: the order amount in cents

    Returns a mapping from ``YYYY‑MM‑DD`` to the summed ``amount_cents`` for that day.
    Days with no orders are omitted from the result.
    """
    revenue_by_day: Dict[str, int] = {}
    for order in orders:
        day = business_day(order["ts"])
        revenue_by_day[day] = revenue_by_day.get(day, 0) + order["amount_cents"]
    return revenue_by_day
