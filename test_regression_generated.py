import pytest
from hypothesis import given, strategies as st

from commandcenter.finops import project_month_end, over_budget


def test_projection_day_one_no_error_and_correct_value():
    # On the first day, the projection should be spend_so_far multiplied by the month length.
    spend = 123
    day = 1
    days_in_month = 30
    expected = round((spend / day) * days_in_month)  # = spend * days_in_month
    assert project_month_end(spend, day, days_in_month) == expected


def test_projection_day_two_not_double():
    # On the second day, the daily rate should be averaged over two days, not one.
    spend = 200
    day = 2
    days_in_month = 30
    expected = round((spend / day) * days_in_month)  # daily = 100, projection = 3000
    assert project_month_end(spend, day, days_in_month) == expected
    # Verify that the result is exactly half of what the buggy version would have produced
    buggy_result = round((spend / (day - 1)) * days_in_month)  # would divide by 1
    assert project_month_end(spend, day, days_in_month) * 2 == buggy_result


@pytest.mark.parametrize(
    "projection,budget,expected",
    [
        (1500, 2000, False),
        (2500, 2500, False),
        (3000, 2500, True),
    ],
)
def test_over_budget_logic(projection, budget, expected):
    assert over_budget(projection, budget) is expected


@given(
    spend=st.integers(min_value=0, max_value=1_000_000),
    delta=st.integers(min_value=0, max_value=1_000_000),
    day=st.integers(min_value=1, max_value=31),
    days_in_month=st.integers(min_value=1, max_value=31),
)
def test_projection_monotonic_in_spend(spend, delta, day, days_in_month):
    """Increasing spend_so_far should never decrease the projected month‑end spend."""
    proj1 = project_month_end(spend, day, days_in_month)
    proj2 = project_month_end(spend + delta, day, days_in_month)
    assert proj1 <= proj2
