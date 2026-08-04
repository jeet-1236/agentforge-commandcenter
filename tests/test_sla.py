"""SLA at-risk tests (cc-code-2).

`test_ticket_at_exactly_the_warning_threshold_is_flagged` is the REPRODUCTION TARGET: a ticket exactly
WARN_MINUTES from its deadline must be flagged at-risk so the desk gets an early warning. It fails on the shipped
strict-'<' check and passes once the boundary is inclusive. Isolated to this bug.
"""
from commandcenter import sla


def test_breached_detection():
    assert sla.is_breached({"id": "T", "sla_minutes": 60, "age_minutes": 60, "status": "open"}) is True
    assert sla.is_breached({"id": "T", "sla_minutes": 60, "age_minutes": 10, "status": "open"}) is False


def test_comfortably_within_sla_not_flagged():
    # 50 min remaining (> 30 warn window) → not at risk
    assert sla.at_risk([{"id": "T1", "sla_minutes": 60, "age_minutes": 10, "status": "open"}]) == []


def test_resolved_ticket_never_at_risk():
    assert sla.at_risk([{"id": "T1", "sla_minutes": 60, "age_minutes": 45, "status": "resolved"}]) == []


def test_ticket_at_exactly_the_warning_threshold_is_flagged():
    # remaining == 30 == WARN_MINUTES: the ticket is exactly at the warning line and MUST be flagged, not slip
    # silently to a breach. The shipped strict-'<' check misses it.
    tickets = [{"id": "T1", "sla_minutes": 60, "age_minutes": 30, "status": "open"}]
    assert sla.at_risk(tickets) == ["T1"]
