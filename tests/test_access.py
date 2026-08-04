"""Access-review tests (cc-code-4).

`test_departed_but_recently_active_is_flagged` is the REPRODUCTION TARGET: a departed employee who was recently
active must still be flagged for access removal. It fails on the shipped 'and' and passes once the condition is
'or'. The other cases stay green as a baseline the fix must not regress. Isolated to this bug.
"""
from commandcenter import access


def test_active_current_employee_not_flagged():
    assert access.needs_review({"id": "u1", "role": "analyst", "departed": False, "days_since_active": 1}) is False


def test_departed_and_dormant_is_flagged():
    # both arms true → flagged on the shipped code AND after the fix (a stable baseline)
    assert access.needs_review({"id": "u2", "role": "admin", "departed": True, "days_since_active": 200}) is True


def test_review_list_collects_flagged_ids():
    users = [{"id": "ok", "departed": False, "days_since_active": 2},
             {"id": "gone", "departed": True, "days_since_active": 200}]   # departed + dormant → flagged either way
    assert access.review_list(users) == ["gone"]


def test_departed_but_recently_active_is_flagged():
    # a contractor who left last month but logged in three days ago must STILL be flagged for access removal.
    # The shipped 'and' hides them because they were recently active.
    assert access.needs_review({"id": "u_leaver", "role": "admin", "departed": True, "days_since_active": 3}) is True
