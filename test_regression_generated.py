import pytest
from commandcenter.sync import sync_records
from hypothesis import given, strategies as st


def test_all_records_sync_successfully():
    records = ["a", "b", "c"]
    # push never raises
    def push(record):
        return f"pushed {record}"
    result = sync_records(records, push)
    assert result == {"synced": 3, "failed": 0}


def test_mixed_success_and_failure():
    records = [1, 2, 3, 4, 5]

    def push(record):
        if record % 2 == 0:  # even numbers fail
            raise RuntimeError("failed")
        return record * 10

    result = sync_records(records, push)
    # odds succeed (1,3,5) -> 3 synced, evens fail (2,4) -> 2 failed
    assert result == {"synced": 3, "failed": 2}


@given(st.lists(st.integers()))
def test_synced_plus_failed_equals_total(records):
    """
    For any list of integers, the sum of synced and failed counts
    must equal the number of input records.
    """
    def push(record):
        if record < 0:
            raise ValueError("negative value")
        return record

    summary = sync_records(records, push)
    assert summary["synced"] + summary["failed"] == len(records)
    # Additional sanity checks
    assert 0 <= summary["synced"] <= len(records)
    assert 0 <= summary["failed"] <= len(records)
