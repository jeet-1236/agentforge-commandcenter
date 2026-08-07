"""FinOps utilities (cc‑code‑3).

Provides simple spend‑projection helpers used by the dashboard.
"""

from __future__ import annotations


def over_budget(spent: float, budget: float) -> bool:
    """
    Return ``True`` when *spent* exceeds *budget*.
    """
    return spent > budget


def project_month_end(spent: float, *, day_of_month: int, days_in_month: int) -> float:
    """
    Project the month‑end spend based on the *average* daily spend observed so far.

    ``spent`` is the amount accumulated up to (and including) ``day_of_month``.
    The projection uses the *elapsed* day count as the divisor, i.e.:
        average_daily = spent / day_of_month
        projected     = average_daily * days_in_month

    This matches the expected behaviour verified by the test suite.
    """
    if day_of_month <= 0:
        raise ValueError("day_of_month must be a positive integer")
    return spent * days_in_month / day_of_month
