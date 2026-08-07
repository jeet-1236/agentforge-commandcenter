"""commandcenter.sla — Service Level Agreement helpers for the Support surface."""
from __future__ import annotations

WARN_MINUTES = 30  # Warning threshold: tickets with this much or less remaining are at risk.


def _open(ticket: dict) -> bool:
    """A ticket is considered open if its status is exactly 'open'."""
    return ticket.get("status") == "open"


def is_breached(ticket: dict) -> bool:
    """Return True if the ticket's age meets or exceeds its SLA limit."""
    if not _open(ticket):
        return False
    return ticket.get("age_minutes", 0) >= ticket.get("sla_minutes", 0)


def at_risk(tickets: list) -> list:
    """
    Return a list of ticket IDs that are at risk of breaching.

    A ticket is at risk if:
      * it is open,
      * and the remaining minutes (sla - age) are **less than or equal to** WARN_MINUTES.
    """
    at_risk_ids = []
    for ticket in tickets:
        if not _open(ticket):
            continue
        remaining = ticket.get("sla_minutes", 0) - ticket.get("age_minutes", 0)
        if remaining <= WARN_MINUTES:
            at_risk_ids.append(ticket.get("id"))
    return at_risk_ids
