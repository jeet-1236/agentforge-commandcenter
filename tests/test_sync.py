import pytest
from commandcenter.sync import sync_records


def _push(record):
    if record.get("id") == "bad":
        raise ValueError("CRM rejected the record")
    return True


def test_all_good_records_sync():
    res = sync_records([{"id": "a"}, {"id": "b"}], _push)
    assert res == {"synced": 2, "failed": 0}


def test_failed_records_are_reported_not_counted_as_synced():
    # a rejected record must show up as FAILED — operators re-run based on this number
    res = sync_records([{"id": "a"}, {"id": "bad"}, {"id": "c"}], _push)
    assert res["synced"] == 2
    assert res["failed"] == 1
