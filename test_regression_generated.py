import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "A", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "A", "name": "Deal A", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        {"id": "B", "name": "Deal B", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 1000 + 2000


def test_pipeline_total_ignores_closed_and_counts_open_once():
    rows = [
        {"id": "C", "name": "Deal C", "amount_usd": 1500, "currency": "JPY", "stage": "closed_won"},
        {"id": "C", "name": "Deal C", "amount_usd": 1500, "currency": "CHF", "stage": "closed_lost"},
        {"id": "D", "name": "Deal D", "amount_usd": 2500, "currency": "USD", "stage": "negotiation"},
    ]
    # Only deal D is open; duplicate closed rows for C should not affect total.
    assert pipeline_total(rows) == 2500


def test_is_open_recognises_open_stages():
    for stage in OPEN_STAGES:
        assert is_open({"stage": stage}) is True
    assert is_open({"stage": "closed_won"}) is False
    assert is_open({"stage": "closed_lost"}) is False
    assert is_open({}) is False


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_rows(rows):
    total = pipeline_total(rows)
    sum_open = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= sum_open
