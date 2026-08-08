import pytest
from hypothesis import given, strategies as st

from commandcenter import pipeline


# Example‑based regression tests ----------------------------------------------

def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "A", "name": "Deal A", "amount_usd": 100, "currency": "USD", "stage": "prospect"},
        # same deal appears again for a different currency, still open
        {"id": "A", "name": "Deal A", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        # another open deal
        {"id": "B", "name": "Deal B", "amount_usd": 250, "currency": "USD", "stage": "qualified"},
        # closed deal should be ignored even if duplicated
        {"id": "C", "name": "Deal C", "amount_usd": 500, "currency": "USD", "stage": "closed_won"},
        {"id": "C", "name": "Deal C", "amount_usd": 500, "currency": "EUR", "stage": "closed_won"},
    ]
    assert pipeline.pipeline_total(rows) == 100 + 250  # each open id counted once


def test_pipeline_total_ignores_non_open_stages():
    rows = [
        {"id": "D", "name": "Deal D", "amount_usd": 300, "currency": "USD", "stage": "negotiation"},
        {"id": "E", "name": "Deal E", "amount_usd": 400, "currency": "USD", "stage": "closed_lost"},
        {"id": "F", "name": "Deal F", "amount_usd": 150, "currency": "USD", "stage": "proposal"},
        {"id": "F", "name": "Deal F", "amount_usd": 150, "currency": "JPY", "stage": "closed_lost"},
    ]
    # Only D and F (open stage) should contribute, each once
    assert pipeline.pipeline_total(rows) == 300 + 150


# Property‑based test ---------------------------------------------------------

@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(pipeline.OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_is_bounded_by_sum_of_open_rows(rows):
    """
    The total returned by pipeline_total cannot exceed the sum of the
    `amount_usd` values of all rows that are in an open stage,
    because duplicates are de‑duplicated by deal id.
    """
    total = pipeline.pipeline_total(rows)
    open_sum = sum(
        int(r["amount_usd"])
        for r in rows
        if r.get("stage") in pipeline.OPEN_STAGES
    )
    assert 0 <= total <= open_sum
