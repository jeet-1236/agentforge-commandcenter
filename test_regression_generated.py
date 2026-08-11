import pytest
from commandcenter.sync import sync_records

def test_sync_records_counts_success_and_failure():
    # Prepare a list of records and a push function that fails on specific items
    records = ["a", "b", "c", "d"]
    fail_on = {"b", "d"}

    def push(record):
        if record in fail_on:
            raise RuntimeError("push failed")
        # otherwise succeed silently

    summary = sync_records(records, push)
    assert summary == {"synced": 2, "failed": 2}
    # Ensure that the failed records are NOT counted as synced
    assert summary["synced"] + summary["failed"] == len(records)

def test_sync_records_all_success():
    records = [1, 2, 3]
    def push(_):
        pass  # never raises

    summary = sync_records(records, push)
    assert summary == {"synced": 3, "failed": 0}

def test_sync_records_all_failure():
    records = ["x", "y"]
    def push(_):
        raise Exception("always fails")

    summary = sync_records(records, push)
    assert summary == {"synced": 0, "failed": 2}

# Property‑based test: for any list of integers, push fails on negatives
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sync_records_invariant_counts(int_list):
    def push(value):
        if value < 0:
            raise ValueError("negative not allowed")
        # success otherwise

    result = sync_records(int_list, push)
    # Number of successful pushes equals count of non‑negative values
    expected_synced = sum(1 for v in int_list if v >= 0)
    expected_failed = sum(1 for v in int_list if v < 0)
    assert result["synced"] == expected_synced
    assert result["failed"] == expected_failed
    # Total must match input length
    assert result["synced"] + result["failed"] == len(int_list)
