"""Pipeline‑rollup utilities (cc-code-1)."""

# Stages considered "open" for pipeline calculations
_OPEN_STAGES = {"proposal", "qualified", "negotiation", "review"}


def is_open(row: dict) -> bool:
    """Return True if the deal row is in an open stage."""
    return row.get("stage") in _OPEN_STAGES


def pipeline_total(rows: list[dict]) -> int:
    """
    Return the total USD amount of all open deals, counting each deal (by its unique ``id``) only once.

    Deals may appear multiple times (e.g., one row per currency). The function deduplicates
    on ``id`` before summing ``amount_usd``.
    """
    seen: set[str] = set()
    total = 0
    for row in rows:
        if not is_open(row):
            continue
        deal_id = row.get("id")
        if deal_id and deal_id not in seen:
            seen.add(deal_id)
            total += int(row.get("amount_usd", 0))
    return total
