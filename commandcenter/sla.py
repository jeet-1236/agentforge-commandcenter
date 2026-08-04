"""commandcenter.sla — SLA breach + at-risk computation for the Support surface.

A ticket is {"id": str, "sla_minutes": int, "age_minutes": int, "status": str}. `remaining = sla - age`.
A ticket is "breached" once age >= sla, and "at risk" while it is still open and within WARN_MINUTES of the
deadline (so the desk gets an early warning before it actually breaches).
"""
from __future__ import annotations

WARN_MINUTES = 30    # flag a ticket as at-risk once it is within 30 minutes of its SLA deadline


def _open(t) -> bool:
    return t.get("status") not in ("resolved", "closed")


def is_breached(t) -> bool:
    return _open(t) and int(t["age_minutes"]) >= int(t["sla_minutes"])


def at_risk(tickets) -> list:
    """Ids of OPEN, not-yet-breached tickets within WARN_MINUTES of their deadline.

    KNOWN-ISSUE (cc-code-2): the check uses a STRICT '<', so a ticket sitting EXACTLY at the warning threshold
    (remaining == WARN_MINUTES) is not flagged — it jumps straight from 'fine' to 'breached' with no early
    warning. The boundary must be inclusive ('<=').
    """
    out = []
    for t in tickets:
        if not _open(t) or is_breached(t):
            continue
        remaining = int(t["sla_minutes"]) - int(t["age_minutes"])
        if remaining < WARN_MINUTES:      # BUG: strict '<' misses the ticket at exactly WARN_MINUTES from breach
            out.append(t["id"])
    return out
