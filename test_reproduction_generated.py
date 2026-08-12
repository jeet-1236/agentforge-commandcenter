import pytest
from commandcenter.reports import business_day


def test_business_day_uses_utc_date_for_early_timestamp():
    # Order timestamp before 05:00 UTC should belong to the same UTC calendar day
    ts = "2026-08-12T02:10:00Z"
    assert business_day(ts) == "2026-08-12"


def test_business_day_uses_utc_date_for_later_timestamp():
    # Order timestamp after 05:00 UTC should also belong to its UTC calendar day
    ts = "2026-08-12T15:00:00Z"
    assert business_day(ts) == "2026-08-12"
