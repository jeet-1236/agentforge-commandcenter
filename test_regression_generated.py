import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_deduplicates_multi_currency_deals():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 150, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 150, "currency": "GBP", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 300, "currency": "USD", "stage": "proposal"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 400, "currency": "JPY", "stage": "negotiation"},
    ]
    # Only one entry per distinct open deal should be counted.
    assert pipeline_total(rows) == 150 + 300 + 400


def test_pipeline_total_ignores_closed_and_duplicates():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 120, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 120, "currency": "EUR", "stage": "closed_won"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 250, "currency": "USD", "stage": "closed_lost"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 500, "currency": "GBP", "stage": "qualified"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 500, "currency": "GBP", "stage": "qualified"},
    ]
    # deal-1 counted once (open row), deal-2 excluded (closed), deal-3 counted once despite duplicate rows.
    assert pipeline_total(rows) == 120 + 500


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    (*OPEN_STAGES, "closed_won", "closed_lost", "other_stage")
                ),
            }
        ),
        max_size=50,
    )
)
def test_pipeline_total_never_exceeds_naive_sum(rows):
    """
    For any feed, the deduped total must be less than or equal to the naive
    sum of all open rows (which may double‑count multi‑currency deals).
    """
    naive_sum = sum(
        int(r["amount_usd"]) for r in rows if is_open(r)
    )
    assert pipeline_total(rows) <= naive_sum
    # Result should never be negative.
    assert pipeline_total(rows) >= 0
