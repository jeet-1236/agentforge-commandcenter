import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    rows = [
        {"id": "deal-1", "name": "Acme", "amount_usd": 150, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-1", "name": "Acme", "amount_usd": 150, "currency": "GBP", "stage": "prospect"},
        {"id": "deal-2", "name": "Beta", "amount_usd": 200, "currency": "USD", "stage": "qualified"},
    ]
    # deal-1 appears twice with full amount, should be counted once (150)
    # deal-2 appears once (200)
    assert pipeline_total(rows) == 150 + 200


def test_closed_and_open_deals_mixed():
    rows = [
        {"id": "d1", "name": "Alpha", "amount_usd": 100, "currency": "USD", "stage": "closed_won"},
        {"id": "d2", "name": "Beta", "amount_usd": 250, "currency": "EUR", "stage": "negotiation"},
        {"id": "d3", "name": "Gamma", "amount_usd": 300, "currency": "GBP", "stage": "closed_lost"},
        {"id": "d2", "name": "Beta", "amount_usd": 250, "currency": "GBP", "stage": "negotiation"},
    ]
    # Only d2 is open; it appears twice, should be counted once.
    assert pipeline_total(rows) == 250


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_is_bounded_by_sum_of_open_amounts(rows):
    total = pipeline_total(rows)
    # total must be non‑negative
    assert total >= 0
    # total cannot exceed the sum of amounts for rows that are open
    open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert total <= open_sum
    # calling again yields the same result (idempotence)
    assert pipeline_total(rows) == total
