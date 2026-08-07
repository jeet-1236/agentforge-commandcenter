"""Pipeline utilities (cc‑code‑1).

Functions for working with sales‑pipeline data, including deduplication of
multi‑currency deal rows.
"""

from __future__ import annotations
from typing import Iterable, Mapping, Set


# Stages that indicate a deal is *closed* and therefore should not contribute
# to the open‑pipeline total.
_CLOSED_STAGES = {"closed_won", "closed_lost", "closed"}


def is_open(deal: Mapping) -> bool:
    """
    Return ``True`` if the supplied *deal* row represents an open pipeline
    opportunity. Anything in ``_CLOSED_STAGES`` is considered closed.
    """
    stage = str(deal.get("stage", "")).lower()
    return stage not in _CLOSED_STAGES


def pipeline_total(rows: Iterable[Mapping]) -> float:
    """
    Compute the total USD value of the open pipeline, counting each distinct
    deal **once** regardless of how many currency rows it appears in.

    Only rows for which :func:`is_open` returns ``True`` are considered. The
    first encountered amount for a given ``id`` is used; subsequent rows with
    the same ``id`` are ignored.
    """
    total = 0.0
    seen_ids: Set = set()
    for row in rows:
        deal_id = row.get("id")
        if not deal_id or deal_id in seen_ids:
            continue
        if is_open(row):
            total += float(row.get("amount_usd", 0))
        # Record the id regardless of openness to avoid double‑counting later.
        seen_ids.add(deal_id)
    return total
