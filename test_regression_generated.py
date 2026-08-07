import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open

# Example regression tests ----------------------------------------------------


def test_pipeline_total_single_open_deal():
    rows = [
        {"id": "D1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 1000


def test_pipeline_total_multi_currency_no_double_count():
    rows = [
        {"id": "D2", "name": "Deal Two", "amount_usd": 5000, "currency": "EUR", "stage": "qualified"},
        {"id": "D2", "name": "Deal Two", "amount_usd": 5000, "currency": "JPY", "stage": "qualified"},
        # closed rows should be ignored even if they have the same id
        {"id": "D2", "name": "Deal Two", "amount_usd": 5000, "currency": "GBP", "stage": "closed_won"},
        # another distinct open deal
        {"id": "D3", "name": "Deal Three", "amount_usd": 2000, "currency": "USD", "stage": "proposal"},
    ]
    # D2 should be counted once (5000) and D3 once (2000) => 7000
    assert pipeline_total(rows) == 7000


def test_is_open_behavior():
    open_row = {"stage": "negotiation"}
    closed_row = {"stage": "closed_lost"}
    missing_stage = {}
    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(missing_stage) is False


# Property‑based test ---------------------------------------------------------


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "JPY", "GBP"]),
                "stage": st.sampled_from(
                    ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
                ),
            }
        ),
        min_size=0,
        max_size=20,
    )
)
def test_pipeline_total_is_consistent_with_open_sum(rows):
    """pipeline_total must never exceed the sum of amounts of open rows,
    and must be non‑negative."""
    total = pipeline_total(rows)
    open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= open_sum
