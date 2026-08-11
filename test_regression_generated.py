import pytest
from hypothesis import given, strategies as st

from commandcenter.retention import is_expired, expired_records


def test_is_expired_on_boundary():
    # Exactly on the retention day should be considered expired
    assert is_expired(10, 10) is True
    # One day before the retention window ends should NOT be expired
    assert is_expired(9, 10) is False


def test_expired_records_filters_correctly():
    records = [
        {"id": 1, "age_days": 7},
        {"id": 2, "age_days": 5},
        {"id": 3, "age_days": 4},
        {"id": 4, "age_days": 10},
    ]
    retention = 5
    expired = expired_records(records, retention)
    # Ages 5,7,10 are >= retention and should be returned
    expected_ids = {1, 2, 4}
    assert {r["id"] for r in expired} == expected_ids
    # Ensure no non‑expired record appears
    assert all(r["age_days"] >= retention for r in expired)


@given(st.integers(min_value=0, max_value=1_000), st.integers(min_value=0, max_value=1_000))
def test_is_expired_is_equivalent_to_comparison(age_days, retention_days):
    # The function should behave exactly like the >= comparison
    assert is_expired(age_days, retention_days) == (age_days >= retention_days)
