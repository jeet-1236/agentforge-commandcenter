import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_deal_ids_are_counted_once():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    # deal-1 appears twice (different currencies) but should be counted once.
    assert pipeline_total(rows) == 1000 + 2000


def test_closed_stages_are_ignored_even_if_id_is_duplicate():
    rows = [
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "GBP", "stage": "closed_won"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "GBP", "stage": "prospect"},
        {"id": "deal-4", "name": "Deal Four", "amount_usd": 2500, "currency": "JPY", "stage": "closed_lost"},
        {"id": "deal-5", "name": "Deal Five", "amount_usd": 3000, "currency": "USD", "stage": "negotiation"},
    ]
    # Only open deals (deal-3 in prospect stage and deal-5) should contribute.
    assert pipeline_total(rows) == 1500 + 3000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        )
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_amounts(rows):
    total = pipeline_total(rows)
    bound = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= bound
