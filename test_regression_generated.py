import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    """A deal appearing in two currencies should contribute only once to the total."""
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 1000


def test_closed_stage_deal_is_ignored_even_if_duplicate():
    """Closed deals must be ignored regardless of duplication."""
    rows = [
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "USD", "stage": "closed_won"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "EUR", "stage": "closed_won"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 1500, "currency": "USD", "stage": "qualified"},
    ]
    # Only deal-3 is open, so total should be its amount.
    assert pipeline_total(rows) == 1500


def test_duplicate_rows_same_id_count_once():
    """Exact duplicate rows must not inflate the total."""
    rows = [
        {"id": "deal-4", "name": "Deal Four", "amount_usd": 500, "currency": "USD", "stage": "proposal"},
        {"id": "deal-4", "name": "Deal Four", "amount_usd": 500, "currency": "USD", "stage": "proposal"},
        {"id": "deal-5", "name": "Deal Five", "amount_usd": 800, "currency": "GBP", "stage": "negotiation"},
    ]
    assert pipeline_total(rows) == 1300  # 500 + 800, not 1500


@given(
    rows=st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=10),
                "name": st.text(min_size=1, max_size=20),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_amounts(rows):
    """
    For any collection of rows, the pipeline total must never be greater than the
    sum of the amounts of rows that are open, because duplicate deal ids are deduplicated.
    """
    open_amount_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert pipeline_total(rows) <= open_amount_sum
