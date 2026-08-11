from datetime import datetime
from commandcenter.sla_clock import business_minutes_between, has_breached

FRI_16 = datetime(2026, 8, 7, 16, 0)     # Friday 16:00
MON_10 = datetime(2026, 8, 10, 10, 0)    # the following Monday 10:00


def test_the_clock_does_not_run_overnight_or_at_the_weekend():
    # Fri 16:00→17:00 (60) + Mon 09:00→10:00 (60) = 120 business minutes, NOT the whole weekend
    assert business_minutes_between(FRI_16, MON_10) == 120


def test_a_plain_working_morning_counts_normally():
    assert business_minutes_between(datetime(2026, 8, 5, 9, 0), datetime(2026, 8, 5, 11, 0)) == 120


def test_a_full_working_day_consumes_an_eight_hour_target():
    assert has_breached(datetime(2026, 8, 5, 9, 0), datetime(2026, 8, 5, 17, 0), 480) is True
