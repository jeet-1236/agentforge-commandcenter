from commandcenter.reports import business_day

def test_business_day_uses_utc_timestamp():
    # Early UTC time that should belong to the same calendar day
    early_ts = "2026-08-12T02:10:00Z"
    assert business_day(early_ts) == "2026-08-12"

    # Typical daytime UTC time that is already correct
    midday_ts = "2026-08-12T15:00:00Z"
    assert business_day(midday_ts) == "2026-08-12"
