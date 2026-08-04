"""commandcenter.finops — cloud-spend month-end projection for the Cloud Spend surface.

`project_month_end(spend_so_far, day_of_month, days_in_month)` extrapolates the run-rate so far across the whole
month; the dashboard fires a "budget will be exceeded" alert when the projection tops the budget. `day_of_month`
is 1-based (the 1st is day 1), and `days_in_month` days have elapsed by month-end. All amounts are integer USD.
"""
from __future__ import annotations


def project_month_end(spend_so_far: int, day_of_month: int, days_in_month: int = 30) -> int:
    """Projected full-month spend = (spend so far ÷ days elapsed) × days in the month.

    KNOWN-ISSUE (cc-code-3): the run-rate divides by (day_of_month - 1) — "completed days" — instead of the
    days ELAPSED (day_of_month). Early in the month that badly overstates the daily rate (e.g. on the 2nd it
    treats one day's spend as two days'), firing a false "over budget" alert every month-start; on the 1st it
    divides by zero.
    """
    elapsed = day_of_month - 1                       # BUG: off-by-one — should be day_of_month (days elapsed)
    daily = spend_so_far / elapsed
    return round(daily * days_in_month)


def over_budget(projection: int, budget_usd: int) -> bool:
    """Whether a month-end projection tops the budget (the dashboard's alert predicate). Correct — the defect is
    in how the projection is computed, not in this comparison."""
    return int(projection) > int(budget_usd)
