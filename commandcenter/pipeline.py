"""commandcenter.pipeline — the Revenue/Deals pipeline‑value rollup shown on the dashboard.

The pipeline total is the sum of the USD value of all open deals. Each deal may appear in the
source data multiple times (e.g., once per currency), but it should only be counted once.
"""

from __future__ import annotations
from typing import Iterable, Dict, Any


def is_open(row: Dict[str, Any]) -> bool:
    """A deal row is considered open if its stage is not a closed stage."""
    stage = row.get("stage", "").lower()
    return not stage.startswith("closed")


def pipeline_total(rows: Iterable[Dict[str, Any]]) -> int:
    """
    Return the total USD amount of all *open* deals, counting each unique deal ID only once.

    Each input row is a dict that contains at least:
        - ``id``: the deal identifier
        - ``amount_usd``: the deal value expressed in USD cents
        - ``stage``: the deal stage (used by :func:`is_open`)

    The function deduplicates rows by ``id`` before summing.
    """
    total = 0
    seen_ids = set()

    for row in rows:
        if not is_open(row):
            continue
        deal_id = row.get("id")
        if deal_id in seen_ids:
            continue
        seen_ids.add(deal_id)
        total += int(row.get("amount_usd", 0))

    return total
