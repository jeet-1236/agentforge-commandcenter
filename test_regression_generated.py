import pytest
from hypothesis import given, strategies as st

import commandcenter.pipeline as pipeline


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "1", "name": "Deal A", "amount_usd": 100, "currency": "USD", "stage": "prospect"},
        {"id": "2", "name": "Deal B", "amount_usd": 200, "currency": "EUR", "stage": "qualified"},
        # duplicate currency rows for deal 1 (should be ignored)
        {"id": "1", "name": "Deal A", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        # duplicate currency rows for deal 2 (should be ignored)
        {"id": "2", "name": "Deal B", "amount_usd": 200, "currency": "JPY", "stage": "qualified"},
    ]
    assert pipeline.pipeline_total(rows) == 300


def test_pipeline_total_ignores_closed_and_missing_ids():
    rows = [
        {"id": "1", "name": "Open Deal", "amount_usd": 150, "currency": "USD", "stage": "proposal"},
        {"id": "2", "name": "Closed Won", "amount_usd": 400, "currency": "EUR", "stage": "closed_won"},
        {"id": None, "name": "No ID", "amount_usd": 999, "currency": "JPY", "stage": "prospect"},
        # duplicate of open deal with different amount (should still count only once, using first occurrence)
        {"id": "1", "name": "Open Deal", "amount_usd": 300, "currency": "EUR", "stage": "proposal"},
    ]
    # Only the first row contributes
    assert pipeline.pipeline_total(rows) == 150


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=1000),
                "currency": st.text(min_size=3, max_size=3),
                "stage": st.sampled_from(
                    list(pipeline.OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
            }
        ),
        max_size=50,
    )
)
def test_pipeline_total_never_exceeds_naive_open_sum(rows):
    """The pipeline total must never be larger than the naive sum of all open rows,
    because duplicate deal IDs are de‑duplicated."""
    naive_open_sum = sum(r["amount_usd"] for r in rows if r["stage"] in pipeline.OPEN_STAGES)
    assert pipeline.pipeline_total(rows) <= naive_open_sum
