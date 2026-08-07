import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open


def test_duplicate_currency_rows_count_once():
    rows = [
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 100,
            "currency": "USD",
            "stage": "prospect",
        },
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 100,
            "currency": "EUR",
            "stage": "prospect",
        },
        {
            "id": "deal-2",
            "name": "Deal Two",
            "amount_usd": 200,
            "currency": "GBP",
            "stage": "qualified",
        },
    ]
    # deal-1 appears twice (different currencies) but should be counted once.
    assert pipeline_total(rows) == 100 + 200


def test_mixed_open_and_closed_deals():
    rows = [
        {
            "id": "a",
            "name": "Alpha",
            "amount_usd": 50,
            "currency": "USD",
            "stage": "prospect",
        },
        {
            "id": "b",
            "name": "Beta",
            "amount_usd": 30,
            "currency": "EUR",
            "stage": "closed_won",  # closed, should be ignored
        },
        {
            "id": "a",
            "name": "Alpha",
            "amount_usd": 50,
            "currency": "CAD",
            "stage": "prospect",
        },
        {
            "id": "c",
            "name": "Gamma",
            "amount_usd": 20,
            "currency": "GBP",
            "stage": "qualified",
        },
    ]
    # Open deals: a (50) and c (20). b is closed, duplicate a counted once.
    assert pipeline_total(rows) == 70


# Property-based test: pipeline_total never exceeds the sum of amounts of all open rows.
@given(
    rows=st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=10),
                "name": st.text(min_size=0, max_size=20),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.text(min_size=3, max_size=3),
                "stage": st.sampled_from(
                    [
                        "prospect",
                        "qualified",
                        "proposal",
                        "negotiation",
                        "closed_won",
                        "closed_lost",
                    ]
                ),
            }
        ),
        max_size=50,
    )
)
def test_pipeline_total_is_not_greater_than_open_sum(rows):
    open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert pipeline_total(rows) <= open_sum
