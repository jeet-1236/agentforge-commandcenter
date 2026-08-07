import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_basic_open_and_closed():
    rows = [
        {
            "id": "1",
            "name": "Deal A",
            "amount_usd": 100,
            "currency": "USD",
            "stage": "prospect",
        },
        {
            "id": "2",
            "name": "Deal B",
            "amount_usd": 200,
            "currency": "EUR",
            "stage": "qualified",
        },
        {
            "id": "3",
            "name": "Deal C",
            "amount_usd": 300,
            "currency": "USD",
            "stage": "closed_won",
        },
    ]
    assert pipeline_total(rows) == 300  # only open deals counted


def test_pipeline_total_multi_currency_duplicate_id():
    rows = [
        # Deal 1 appears in two currencies, both rows are open
        {
            "id": "1",
            "name": "Deal A",
            "amount_usd": 500,
            "currency": "USD",
            "stage": "prospect",
        },
        {
            "id": "1",
            "name": "Deal A",
            "amount_usd": 500,
            "currency": "EUR",
            "stage": "prospect",
        },
        # Deal 2 appears open and later closed; should be counted once
        {
            "id": "2",
            "name": "Deal B",
            "amount_usd": 400,
            "currency": "USD",
            "stage": "qualified",
        },
        {
            "id": "2",
            "name": "Deal B",
            "amount_usd": 400,
            "currency": "GBP",
            "stage": "closed_lost",
        },
        # Deal 3 is closed only and should not affect total
        {
            "id": "3",
            "name": "Deal C",
            "amount_usd": 250,
            "currency": "USD",
            "stage": "closed_won",
        },
    ]
    assert pipeline_total(rows) == 900  # 500 (Deal 1) + 400 (Deal 2)


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=3, max_size=3),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        )
    )
)
def test_pipeline_total_is_non_negative_and_not_exceed_open_sum(rows):
    total = pipeline_total(rows)
    open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= open_sum
