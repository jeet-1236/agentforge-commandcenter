"""commandcenter.sla_clock — business-hours SLA clock for the Support surface.

Support runs 09:00–17:00, Monday to Friday. A resolution target of "8 business hours" means eight hours of
WORKING time — nights and weekends must not burn the customer's SLA. This is the single most common SLA
defect in the industry: the clock is computed in calendar time while the target is stated in business hours,
so a ticket raised late on Friday breaches over the weekend without anyone touching it.
"""
from __future__ import annotations

from datetime import datetime, timedelta

BUSINESS_START, BUSINESS_END = 9, 17          # 09:00–17:00
WORKDAYS = (0, 1, 2, 3, 4)                    # Mon–Fri (datetime.weekday())


def business_minutes_between(start: datetime, end: datetime) -> int:
    """Minutes of BUSINESS time between `start` and `end` — outside 09:00–17:00 and at weekends must not count."""
    return int((end - start).total_seconds() // 60)


def has_breached(opened_at: datetime, now: datetime, target_business_minutes: int) -> bool:
    """True once a ticket has consumed its business-hours resolution target."""
    return business_minutes_between(opened_at, now) >= target_business_minutes
