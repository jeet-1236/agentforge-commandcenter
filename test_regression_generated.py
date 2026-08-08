import pytest
from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES

# ---- Example‑based regression tests ----

def test_duplicate_open_rows_count_once():
    rows = [
        {"id": "deal-1", "name": "A", "amount_usd": 100, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "A", "amount_usd": 100, "currency": "EUR", "stage": "proposal"},
    ]
    assert pipeline_total(rows) == 100  # amount counted only once


def test_closed_then_open_row_counts_once():
    rows = [
        {"id": "deal-2", "name": "B", "amount_usd": 200, "currency": "JPY", "stage": "closed_lost"},
        {"id": "deal-2", "name": "B", "amount_usd": 200, "currency": "USD", "stage": "negotiation"},
    ]
    # Only the open row should contribute, and only once
    assert pipeline_total(rows) == 200


def test_only_closed_rows_give_zero_total():
    rows = [
        {"id": "deal-3", "name": "C", "amount_usd": 150, "currency": "GBP", "stage": "closed_won"},
        {"id": "deal-4", "name": "D", "amount_usd": 300, "currency": "EUR", "stage": "closed_lost"},
    ]
    assert pipeline_total(rows) == 0


def test_multiple_distinct_deals_are_summed():
    rows = [
        {"id": "deal-5", "name": "E", "amount_usd": 50, "currency": "USD", "stage": "prospect"},
        {"id": "deal-6", "name": "F", "amount_usd": 75, "currency": "CAD", "stage": "qualified"},
        {"id": "deal-7", "name": "G", "amount_usd": 125, "currency": "EUR", "stage": "negotiation"},
    ]
    assert pipeline_total(rows) == 250


# ---- Property‑based tests using Hypothesis ----

from hypothesis import given, strategies as st


@st.composite
def rows_strategy(draw):
    # generate a random deal id (allow repeats)
    deal_id = draw(st.text(min_size=1, max_size=10))
    # stage can be open or closed
    stage = draw(st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]))
    amount = draw(st.integers(min_value=0, max_value=10_000))
    currency = draw(st.text(min_size=3, max_size=3))  # ISO currency code like 'USD'
    return {
        "id": deal_id,
        "name": draw(st.text(min_size=1, max_size=5)),
        "amount_usd": amount,
        "currency": currency,
        "stage": stage,
    }


@given(st.lists(rows_strategy(), min_size=0, max_size=20))
def test_total_is_not_greater_than_naive_open_sum(rows):
    """The pipeline total must never exceed the naive sum of amounts from open rows."""
    naive_open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    total = pipeline_total(rows)
    assert 0 <= total <= naive_open_sum


@given(st.lists(rows_strategy(), min_size=1, max_size=20))
def test_adding_duplicate_row_does_not_change_total(rows):
    """
    Adding a row that repeats an existing deal id (regardless of stage) must not increase the total.
    """
    original_total = pipeline_total(rows)

    # pick an existing id (if any); otherwise the list is empty which is impossible due to min_size=1
    existing_id = rows[0]["id"]
    duplicate = {
        "id": existing_id,
        "name": "duplicate",
        "amount_usd": rows[0]["amount_usd"],  # same amount, but stage may differ
        "currency": rows[0]["currency"],
        "stage": rows[0]["stage"],
    }
    extended = rows + [duplicate]
    extended_total = pipeline_total(extended)

    assert extended_total == original_total
