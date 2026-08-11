from commandcenter.priority import priority_of, is_major


def test_widespread_outage_that_is_not_urgent_still_outranks_a_single_urgent_user():
    # impact 1 (everyone) + urgency 3 (can wait) is P3 on the matrix; impact 3 + urgency 1 is also P3 —
    # but a widespread MEDIUM-urgency incident must outrank one user's urgent request
    assert priority_of(1, 2) < priority_of(3, 1)


def test_a_company_wide_urgent_incident_is_p1():
    assert priority_of(1, 1) == 1 and is_major(1, 1) is True


def test_a_single_user_low_urgency_request_is_lowest():
    assert priority_of(3, 3) == 4
