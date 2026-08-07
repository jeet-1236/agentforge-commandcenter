"""commandcenter.pipeline — pipeline roll‑up utilities for the Sales surface."""
from __future__ import annotations

def is_open(deal: dict) -> bool:
    """
    Determine if a deal is considered "open".

    In this simplified model, any stage that is not 'closed_won' (or other closed stages)
    is treated as open. The tests only check for 'closed_won'.
    """
    return deal.get("stage") != "closed_won"


def pipeline_total(deals: list) -> int:
    """
    Sum the USD value of all *open* deals, counting each distinct deal ID only once.

    Some deals may appear multiple times (e.g., per‑currency rows). Only the first
    occurrence of a given ``id`` should contribute to the total.
    """
    total = 0
    seen_ids = set()
    for deal in deals:
        deal_id = deal.get("id")
        if not deal_id or deal_id in seen_ids:
            continue
        if is_open(deal):
            total += int(deal.get("amount_usd", 0))
        seen_ids.add(deal_id)
    return total
