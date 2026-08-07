import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_id_counts_once():
    # Same deal appears twice in different currencies, both open stages.
    rows = [
        {"id": "deal-1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal A", "amount_usd": 1000, "currency": "JPY", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 1000  # should count only once


def test_mixed_stages_and_duplicates():
    rows = [
        {"id": "d1", "name": "Deal 1", "amount_usd": 200, "currency": "EUR", "stage": "qualified"},
        {"id": "d2", "name": "Deal 2", "amount_usd": 300, "currency": "GBP", "stage": "closed_won"},
        {"id": "d1", "name": "Deal 1 dup", "amount_usd": 200, "currency": "JPY", "stage": "qualified"},
        {"id": "d3", "name": "Deal 3", "amount_usd": 400, "currency": "USD", "stage": "negotiation"},
        {"id": "d3", "name": "Deal 3 dup", "amount_usd": 400, "currency": "CAD", "stage": "negotiation"},
    ]
    # Only open deals d1 and d3 should be counted once each.
    assert pipeline_total(rows) == 200 + 400


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.one_of(st.none(), st.text(min_size=1)),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_is_not_greater_than_sum_of_open_amounts(rows):
    # Compute naive sum of amount_usd for rows that are open (including duplicates)
    naive_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    # The corrected total should never exceed the naive sum
    assert pipeline_total(rows) <= naive_sum
    # It should be non‑negative
    assert pipeline_total(rows) >= 0
