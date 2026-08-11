"""commandcenter.onhold — resolution-clock accounting for the Support surface.

A ticket parked "awaiting the customer" must PAUSE its resolution clock: the desk cannot be held responsible
for time the customer has the ball. Every major ITSM tool models this, and getting it wrong is how a desk
posts a breach for a ticket it was never able to work on.

`events` is a chronological list of {"status": str, "minutes": int} spans.
"""
from __future__ import annotations

PAUSED_STATUSES = ("on_hold", "awaiting_customer", "awaiting_vendor")


def counted_minutes(events) -> int:
    """Minutes charged against the resolution target — time in a PAUSED status must be excluded."""
    return sum(int(e["minutes"]) for e in events if e["status"] not in PAUSED_STATUSES)
