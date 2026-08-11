import pytest
from hypothesis import given, strategies as st
from commandcenter import retention


def test_is_expired_boundary():
    # Exactly at the retention boundary should be considered expired per the corrected logic
    assert retention.is_expired(age_days=10, retention_days=10) is True
    assert retention.is_expired(age_days=11, retention_days=10) is True
    assert retention.is_expired(age_days=9, retention_days=10) is False


def test_expired_records_filters_mixed_list():
    records = [
        {"id": 1, "age_days": 5},
        {"id": 2, "age_days": 10},
        {"id": 3, "age_days": 15},
        {"id": 4, "age_days": 0},
    ]
    retention_days = 10
    expired = retention.expired_records(records, retention_days)
    # Should contain only records with age_days >= 10
    expected = [
        {"id": 2, "age_days": 10},
        {"id": 3, "age_days": 15},
    ]
    assert expired == expected


@given(
    ages=st.lists(st.integers(min_value=0, max_value=100), min_size=0, max_size=20),
    retention_days=st.integers(min_value=0, max_value=100),
)
def test_expired_records_property(ages, retention_days):
    records = [{"age_days": a, "idx": i} for i, a in enumerate(ages)]
    result = retention.expired_records(records, retention_days)

    # Every returned record must satisfy the expiration condition
    assert all(r["age_days"] >= retention_days for r in result)

    # The result must be exactly the subset of input records that satisfy the condition
    expected = [r for r in records if r["age_days"] >= retention_days]
    assert result == expected
