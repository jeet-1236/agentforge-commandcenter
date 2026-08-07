import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_open_deal_once():
    # Same deal appears twice (different currencies), both open stages
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        # Another distinct open deal
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 500, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 1000 + 500


def test_pipeline_total_ignores_closed_deals_and_duplicates():
    rows = [
        {"id": "d1", "name": "A", "amount_usd": 200, "currency": "USD", "stage": "closed_won"},
        {"id": "d2", "name": "B", "amount_usd": 300, "currency": "EUR", "stage": "closed_lost"},
        {"id": "d3", "name": "C", "amount_usd": 400, "currency": "USD", "stage": "negotiation"},
        {"id": "d3", "name": "C", "amount_usd": 400, "currency": "GBP", "stage": "negotiation"},
    ]
    # Only the open deal d3 should contribute, exactly once
    assert pipeline_total(rows) == 400


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
        min_size=0,
        max_size=20,
    )
)
def test_pipeline_total_is_not_greater_than_sum_of_open_amounts(rows):
    """
    For any collection of rows, the total reported by `pipeline_total` must never
    exceed the sum of `amount_usd` of the rows that are open. Duplicated deal ids are
    de‑duplicated, so the total is bounded above by that sum.
    """
    sum_of_open = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    total = pipeline_total(rows)
    assert 0 <= total <= sum_of_open
    # The result must be an int
    assert isinstance(total, int)
