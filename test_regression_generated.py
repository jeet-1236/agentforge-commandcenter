import pytest
from commandcenter.access import review_list

def test_review_list_sorts_flagged_ids():
    employees = [
        {"id": 3, "departed": True},
        {"id": 1, "departed": True},
        {"id": 2},
        {"id": 4, "departed": False},
    ]
    assert review_list(employees) == [1, 3]

def test_review_list_is_order_independent():
    employees = [
        {"id": 10, "departed": True},
        {"id": 5, "departed": True},
    ]
    reversed_employees = list(reversed(employees))
    assert review_list(employees) == review_list(reversed_employees) == [5, 10]

def test_review_list_empty_input():
    assert review_list([]) == []

# Property‑based test for the pure function
from hypothesis import given, strategies as st

# Strategy for an employee dict where "departed" may be missing
employee_strategy = st.builds(
    lambda emp_id, departed: (
        {"id": emp_id, **({} if departed is None else {"departed": departed})}
    ),
    emp_id=st.integers(min_value=0, max_value=1000),
    departed=st.one_of(st.none(), st.booleans()),
)

@given(st.lists(employee_strategy, max_size=20))
def test_review_list_invariant_sorted_and_correct(employees):
    result = review_list(employees)
    # The result must be sorted in ascending order
    assert result == sorted(result)
    # The result must contain exactly the ids of employees marked as departed
    expected = {e["id"] for e in employees if e.get("departed")}
    assert result == sorted(expected)
