"""FinOps utilities (cc-code-3)."""


def over_budget(spend: int, budget: int) -> bool:
    """Return True if the spend exceeds the budget."""
    return spend > budget


def project_month_end(spend_to_date: int, *, day_of_month: int, days_in_month: int) -> int:
    """
    Project the total spend for the month based on spend to date.

    The projection uses the average daily spend over the days elapsed (including the current day)
    and extrapolates it to the full month length.
    """
    if day_of_month <= 0:
        raise ValueError("day_of_month must be a positive integer")
    # Average spend per elapsed day
    avg_per_day = spend_to_date / day_of_month
    # Projected total for the whole month
    projected = avg_per_day * days_in_month
    return int(projected)
