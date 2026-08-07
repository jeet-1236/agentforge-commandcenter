"""SLA monitoring utilities (cc‑code‑2).

Implements breach detection and at‑risk warning logic for tickets.
"""

from __future__ import annotations
from typing import Iterable, List, Mapping

# Number of minutes before the SLA deadline that constitutes a warning state.
WARN_MINUTES = 30


def is_breached(ticket: Mapping) -> bool:
    """
    Return ``True`` when a ticket has exceeded its SLA.
    Only tickets with a status of ``"open"`` are evaluated.
    """
    if ticket.get("status") != "open":
        return False
    return ticket.get("age_minutes", 0) >= ticket.get("sla_minutes", 0)


def at_risk(tickets: Iterable[Mapping]) -> List[str]:
    """
    Return a list of ticket identifiers that are *at risk* of breaching their SLA.

    A ticket is at risk when:
    * it is ``open``,
    * it has **not** yet breached, and
    * the remaining time (``sla_minutes - age_minutes``) is less than or equal to
      :data:`WARN_MINUTES`.

    The function includes tickets whose remaining time is exactly the warning
    threshold, matching the inclusive boundary required by the tests.
    """
    at_risk_ids: List[str] = []
    for ticket in tickets:
        if ticket.get("status") != "open":
            continue
        if is_breached(ticket):
            continue
        remaining = ticket.get("sla_minutes", 0) - ticket.get("age_minutes", 0)
        if remaining <= WARN_MINUTES:
            at_risk_ids.append(ticket.get("id"))
    return at_risk_ids
