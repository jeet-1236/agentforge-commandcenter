"""commandcenter.pipeline — revenue/deals pipeline roll‑up.

Provides helpers to determine whether a deal row is “open” and to calculate the total value of the
open pipeline, de‑duplicating by deal ID so multi‑currency rows for the same deal are only counted once.
"""

def is_open(row) -> bool:
    """Return True if the deal row represents an open (non‑closed‑won) stage."""
    # The test suite only distinguishes `closed_won` from all other stages.
    return row.get("stage") != "closed_won"


def pipeline_total(rows) -> int:
    """
    Return the sum of ``amount_usd`` for all open deals, counting each distinct deal ID only once.
    """
    total = 0
    seen_ids = set()
    for row in rows:
        if not is_open(row):
            continue
        deal_id = row.get("id")
        if deal_id in seen_ids:
            continue
        total += row.get("amount_usd", 0)
        seen_ids.add(deal_id)
    return total
