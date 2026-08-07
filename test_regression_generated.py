import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_deal_counts_once():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 2500, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 2500, "currency": "GBP", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 2500


def test_closed_stage_is_ignored_even_if_duplicate():
    rows = [
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 4000, "currency": "EUR", "stage": "negotiation"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 4000, "currency": "EUR", "stage": "closed_won"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "USD", "stage": "closed_lost"},
    ]
    # only the open row for deal-2 counts; deal-3 is closed.
    assert pipeline_total(rows) == 4000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1, max_size=3),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]),
            }
        )
    )
)
def test_pipeline_total_not_exceed_sum_of_open(rows):
    total = pipeline_total(rows)
    max_possible = sum(row["amount_usd"] for row in rows if is_open(row))
    assert 0 <= total <= max_possible
