"""Cloud-spend projection tests (cc-code-3).

`test_projection_uses_days_elapsed_not_completed` is the REPRODUCTION TARGET: the month-end projection must use
the daily run-rate over the days ELAPSED, so a normal early-month spend doesn't project a false overage. It fails
on the shipped off-by-one divisor and passes once it divides by the elapsed day count. `over_budget` (the alert
predicate) is correct and stays green — a baseline the fix must not regress. Isolated to this bug.
"""
from commandcenter import finops


def test_over_budget_predicate_is_correct():
    assert finops.over_budget(6000, 5000) is True
    assert finops.over_budget(4000, 5000) is False


def test_projection_uses_days_elapsed_not_completed():
    # Day 2 of the month, $200 spent = $100/day → the projection should be ~$3000 for a 30-day month, NOT ~$6000.
    # The shipped code divides by (day-1)=1 and treats one day's spend as the full daily rate → a false alert.
    assert finops.project_month_end(200, day_of_month=2, days_in_month=30) == 3000
