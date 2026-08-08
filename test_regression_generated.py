import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_is_open_recognizes_open_and_closed_stages():
    open_row = {"id": "1", "stage": "prospect"}
    closed_row = {"id": "2", "stage": "closed_won"}
    unknown_row = {"id": "3", "stage": "something_else"}

    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(unknown_row) is False


def test_pipeline_total_counts_deal_once_per_id_and_excludes_closed():
    rows = [
        # Deal d1 appears in two currencies, both open
        {"id": "d1", "name": "Deal 1", "stage": "prospect", "amount_usd": 100, "currency": "USD"},
        {"id": "d1", "name": "Deal 1", "stage": "prospect", "amount_usd": 100, "currency": "EUR"},
        # Deal d2 is closed – should be ignored
        {"id": "d2", "name": "Deal 2", "stage": "closed_won", "amount_usd": 200, "currency": "USD"},
        # Deal d3 appears in two currencies, both open
        {"id": "d3", "name": "Deal 3", "stage": "qualified", "amount_usd": 300, "currency": "GBP"},
        {"id": "d3", "name": "Deal 3", "stage": "qualified", "amount_usd": 300, "currency": "JPY"},
    ]

    # Only d1 and d3 should contribute, each exactly once
    assert pipeline_total(rows) == 100 + 300


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=0, max_size=10),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_matches_manual_expected(rows):
    """For any collection of rows, pipeline_total should equal the sum of
    amount_usd for each distinct deal id that has at least one open row."""
    expected_by_id = {}
    for r in rows:
        if r["stage"] in OPEN_STAGES:
            # first open occurrence determines the amount for that deal
            expected_by_id.setdefault(r["id"], int(r["amount_usd"]))

    assert pipeline_total(rows) == sum(expected_by_id.values())
