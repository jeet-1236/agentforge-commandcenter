"""commandcenter.access — the access-review check for the Access & Security surface.

A user is {"id": str, "role": str, "departed": bool, "days_since_active": int}. The periodic access review flags
anyone whose access should be revoked or re-attested: a DEPARTED employee, OR anyone dormant past the stale
window (a live account nobody uses is a standing risk).
"""
from __future__ import annotations

STALE_DAYS = 90    # dormant longer than this → flag for review


def needs_review(user) -> bool:
    """Flag a user for the access review.

    KNOWN-ISSUE (cc-code-4): this uses AND, so a DEPARTED employee who was recently active is NOT flagged —
    a leaver who still logs in keeps their access and never appears in the review. A departed user must be flagged
    regardless of recent activity; the condition should be OR.
    """
    departed = bool(user.get("departed"))
    dormant = int(user.get("days_since_active", 0)) > STALE_DAYS
    return departed or dormant  # Fixed: flag if either condition is true


def review_list(users) -> list:
    """Ids of every user the access review should flag."""
    return [u["id"] for u in users if needs_review(u)]
