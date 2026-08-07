import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 3000  # 1000 (deal-1) + 2000 (deal-2), not 4000


def test_closed_stage_is_ignored_even_if_duplicate():
    rows = [
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "USD", "stage": "closed_won"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "EUR", "stage": "closed_won"},
        {"id": "deal-4", "name": "Deal Four", "amount_usd": 2500, "currency": "USD", "stage": "negotiation"},
    ]
    # closed deals are not open, so only deal-4 contributes
    assert pipeline_total(rows) == 2500


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
            }
        ),
        min_size=0,
        max_size=20,
    )
)
def test_pipeline_total_is_not_greater_than_sum_of_open_rows(rows):
    total = pipeline_total(rows)
    sum_open = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= sum_open
