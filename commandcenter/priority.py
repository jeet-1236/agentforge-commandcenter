"""commandcenter.priority — the ITIL impact x urgency priority matrix for intake.

Priority is NOT a single dimension: it is derived from how widely something hurts (impact) and how fast it
must be dealt with (urgency). Deriving it wrongly is how a company-wide outage is queued behind a single
user's password reset. 1 = highest.
"""
from __future__ import annotations

#            urgency: 1(high) 2(med) 3(low)
_MATRIX = {1: {1: 1, 2: 2, 3: 3},          # impact 1 = widespread
           2: {1: 2, 2: 3, 3: 4},          # impact 2 = several users
           3: {1: 3, 2: 4, 3: 4}}          # impact 3 = one user


def priority_of(impact: int, urgency: int) -> int:
    """The ITIL priority for an incident, from the impact x urgency matrix."""
    return _MATRIX[int(impact)][int(urgency)]


def is_major(impact: int, urgency: int) -> bool:
    """A P1 is the major-incident trigger (declares a bridge, pages the on-call)."""
    return priority_of(impact, urgency) == 1
