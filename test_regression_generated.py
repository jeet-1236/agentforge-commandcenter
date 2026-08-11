import pytest
from commandcenter.sync import sync_records

def test_all_success():
    records = [1, 2, 3, 4]
    def push(record):
        # succeed for any record
        return None
    result = sync_records(records, push)
    assert result == {"synced": 4, "failed": 0}

def test_mixed_success_and_failure():
    records = ["a", "b", "c", "d"]
    failures = {"b", "d"}  # these will raise
    def push(record):
        if record in failures:
            raise RuntimeError("failed")
        return None
    result = sync_records(records, push)
    assert result["synced"] == 2
    assert result["failed"] == 2
    # ensure no record is counted twice
    assert result["synced"] + result["failed"] == len(records)

# Property‑based test: total count must equal number of records,
# and counts must match the pattern of successes/failures supplied.
from hypothesis import given, strategies as st

@given(st.lists(st.booleans()))
def test_sync_records_counts_match_boolean_success_pattern(success_flags):
    # Build dummy records; their actual values are irrelevant.
    records = list(range(len(success_flags)))

    # Create a push function that succeeds when the corresponding flag is True,
    # otherwise raises.
    def make_push(flags):
        it = iter(flags)
        def push(_):
            if not next(it):
                raise RuntimeError("failure")
        return push

    push = make_push(success_flags)
    result = sync_records(records, push)

    expected_synced = sum(success_flags)
    expected_failed = len(success_flags) - expected_synced

    assert result["synced"] == expected_synced
    assert result["failed"] == expected_failed
    assert result["synced"] + result["failed"] == len(records)
