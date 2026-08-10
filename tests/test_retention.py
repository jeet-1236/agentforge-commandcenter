from commandcenter.retention import is_expired, expired_records


def test_record_is_not_expired_on_the_final_day_of_the_window():
    # day 29 of a 30-day window is still INSIDE retention — deleting it is a compliance breach
    assert is_expired(29, 30) is False


def test_record_expires_once_the_window_has_passed():
    assert is_expired(30, 30) is True


def test_expired_records_selects_only_the_expired():
    recs = [{"id": 1, "age_days": 29}, {"id": 2, "age_days": 31}]
    assert [r["id"] for r in expired_records(recs, 30)] == [2]
