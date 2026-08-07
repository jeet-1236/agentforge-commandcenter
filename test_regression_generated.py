import pytest
from hypothesis import given, strategies as st

from commandcenter.access import needs_review, review_list, STALE_DAYS


def test_needs_review_departed_recent():
    """A departed employee must be flagged even if they were active recently."""
    user = {"id": "U1", "departed": True, "days_since_active": 1}
    assert needs_review(user) is True


def test_needs_review_dormant_non_departed():
    """A non‑departed user who is dormant longer than the stale window must be flagged."""
    user = {"id": "U2", "departed": False, "days_since_active": STALE_DAYS + 1}
    assert needs_review(user) is True


def test_needs_review_neither_condition():
    """A user who is not departed and not dormant must not be flagged."""
    user = {"id": "U3", "departed": False, "days_since_active": STALE_DAYS - 1}
    assert needs_review(user) is False


def test_review_list_returns_correct_ids():
    """review_list should return ids only for users that need review."""
    users = [
        {"id": "A", "departed": True, "days_since_active": 0},
        {"id": "B", "departed": False, "days_since_active": STALE_DAYS + 5},
        {"id": "C", "departed": False, "days_since_active": 10},
    ]
    result = review_list(users)
    assert result == ["A", "B"]


@given(
    departed=st.booleans(),
    days=st.integers(min_value=0, max_value=1000),
    extra=st.dictionaries(
        keys=st.text(min_size=1, max_size=5),
        values=st.integers(),
        min_size=0,
        max_size=3,
    ),
)
def test_needs_review_invariant(departed, days, extra):
    """
    Invariant: needs_review returns True iff the user is departed
    OR has been inactive longer than STALE_DAYS.
    """
    user = {"id": "x", "departed": departed, "days_since_active": days, **extra}
    result = needs_review(user)
    if departed or days > STALE_DAYS:
        assert result is True
    else:
        assert result is False
