import pytest
from hypothesis import given, strategies as st

from commandcenter.sync import sync_records


def test_all_records_successful():
    """When push never raises, all records should be counted as synced."""
    records = ["a", "b", "c", "d"]

    def push(_):
        return None  # never raises

    result = sync_records(records, push)
    assert result == {"synced": len(records), "failed": 0}


def test_mixed_success_and_failure():
    """Records that cause push to raise are counted as failed, others as synced."""
    records = [1, 2, 3, 4, 5]

    def push(r):
        if r % 2 == 0:  # even numbers fail
            raise RuntimeError("reject")
        return None

    result = sync_records(records, push)
    assert result["synced"] == 3  # 1,3,5
    assert result["failed"] == 2   # 2,4
    assert result["synced"] + result["failed"] == len(records)


@given(
    records=st.lists(st.integers()),
    fail_set=st.sets(st.integers()),
)
def test_sync_records_counts_match_fail_set(records, fail_set):
    """For any list of records and any set of values that should fail, the
    summary must reflect the exact counts of successes and failures."""
    def push(r):
        if r in fail_set:
            raise RuntimeError("forced failure")
        return None

    result = sync_records(records, push)
    expected_failed = sum(1 for r in records if r in fail_set)
    expected_synced = len(records) - expected_failed

    assert result["failed"] == expected_failed
    assert result["synced"] == expected_synced
    assert result["synced"] + result["failed"] == len(records)
