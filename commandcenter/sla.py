"""SLA at‑risk utilities (cc-code-2)."""

WARN_MINUTES = 30  # minutes before deadline when a ticket is considered "at risk"


def is_breached(ticket: dict) -> bool:
    """
    Return True if the ticket is past its SLA deadline.

    A ticket is breached when its age is greater than or equal to the SLA minutes
    and it is still open.
    """
    return (
        ticket.get("status") == "open"
        and ticket.get("age_minutes", 0) >= ticket.get("sla_minutes", 0)
    )


def at_risk(tickets: list[dict]) -> list[str]:
    """
    Return a list of ticket IDs that are within the warning window.

    A ticket is "at risk" when it is open and the remaining time until the SLA deadline
    is less than or **equal to** ``WARN_MINUTES``.
    """
    at_risk_ids: list[str] = []
    for t in tickets:
        if t.get("status") != "open":
            continue
        remaining = t.get("sla_minutes", 0) - t.get("age_minutes", 0)
        if remaining <= WARN_MINUTES:
            at_risk_ids.append(t.get("id"))
    return at_risk_ids
