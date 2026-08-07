"""commandcenter.finops — financial operations helpers for the FinOps surface."""
from __future__ import annotations

def over_budget(spend: int, budget: int) -> bool:
    """Return True if spend exceeds the given budget."""
    return spend > budget


def project_month_end(spend_to_date: int, *, day_of_month: int, days_in_month: int) -> int:
    """
    Project the month‑end spend based on the spend to date.

    The projection should use the *elapsed* days (day_of_month) to compute a daily rate,
    then extrapolate that rate over the full month length (days_in_month).

    Example:
        day_of_month = 2, spend_to_date = 200 → $100/day → $3000 for a 30‑day month.
    """
    if day_of_month <= 0:
        # Avoid division by zero; with no elapsed days we cannot project.
        return 0
    daily_rate = spend_to_date / day_of_month
    projected = daily_rate * days_in_month
    return int(projected)
