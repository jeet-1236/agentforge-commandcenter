import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open


def test_multi_currency_deal_counts_once():
    rows = [
        {"id": "1", "name": "Deal A", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        {"id": "1", "name": "Deal A", "amount_usd": 100, "currency": "GBP", "stage": "prospect"},
        {"id": "2", "name": "Deal B", "amount_usd": 200, "currency": "USD", "stage": "qualified"},
        {"id": "3", "name": "Deal C", "amount_usd": 150, "currency": "JPY", "stage": "closed_won"},
    ]
    # Only open deals (ids 1 and 2) should be counted once each
    assert pipeline_total(rows) == 100 + 200


def test_open_and_closed_rows_same_id():
    rows = [
        {"id": "10", "name": "Deal X", "amount_usd": 500, "currency": "USD", "stage": "closed_lost"},
        {"id": "10", "name": "Deal X", "amount_usd": 500, "currency": "USD", "stage": "prospect"},
        {"id": "11", "name": "Deal Y", "amount_usd": 300, "currency": "EUR", "stage": "closed_won"},
        {"id": "12", "name": "Deal Z", "amount_usd": 400, "currency": "GBP", "stage": "qualified"},
    ]
    # Deal 10 is open despite an earlier closed row, and should be counted once.
    # Deal 11 is closed and ignored. Deal 12 is open.
    assert pipeline_total(rows) == 500 + 400


@given(
    rows=st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
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
        )
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_amounts(rows):
    total = pipeline_total(rows)
    sum_open = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert total <= sum_open
