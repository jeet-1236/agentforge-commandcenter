import pytest
from hypothesis import given, strategies as st

from commandcenter import pipeline


def test_pipeline_total_counts_each_open_deal_once():
    # Two open deals, each appears twice (different currencies) with the same amount_usd.
    rows = [
        {"id": "A1", "name": "Deal A", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "A1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "B2", "name": "Deal B", "amount_usd": 2500, "currency": "GBP", "stage": "qualified"},
        {"id": "B2", "name": "Deal B", "amount_usd": 2500, "currency": "USD", "stage": "qualified"},
    ]
    # Expected total is 1000 + 2500 = 3500 (each deal counted once)
    assert pipeline.pipeline_total(rows) == 3500


def test_pipeline_total_ignores_closed_deals_and_dedupes_ids():
    rows = [
        {"id": "C3", "name": "Deal C", "amount_usd": 500, "currency": "USD", "stage": "closed_won"},
        {"id": "D4", "name": "Deal D", "amount_usd": 800, "currency": "EUR", "stage": "negotiation"},
        {"id": "D4", "name": "Deal D", "amount_usd": 800, "currency": "GBP", "stage": "negotiation"},
        {"id": "E5", "name": "Deal E", "amount_usd": 1200, "currency": "USD", "stage": "closed_lost"},
        {"id": "F6", "name": "Deal F", "amount_usd": 1500, "currency": "USD", "stage": "proposal"},
    ]
    # Only deals D4 and F6 are open; D4 should be counted once.
    # Expected total = 800 (D4) + 1500 (F6) = 2300
    assert pipeline.pipeline_total(rows) == 2300


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(
                    ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
                ),
            }
        ),
        min_size=0,
        max_size=30,
    )
)
def test_pipeline_total_is_not_greater_than_sum_of_open_amounts(rows):
    total = pipeline.pipeline_total(rows)
    open_sum = sum(int(r["amount_usd"]) for r in rows if pipeline.is_open(r))
    # The pipeline total must never exceed the naive sum of all open rows
    assert 0 <= total <= open_sum
