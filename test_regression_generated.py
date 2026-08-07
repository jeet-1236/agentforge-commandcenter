import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_deal_counts_once():
    rows = [
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 100_000,
            "currency": "EUR",
            "stage": "prospect",
        },
        {
            "id": "deal-1",  # same deal, different currency
            "name": "Deal One",
            "amount_usd": 100_000,
            "currency": "GBP",
            "stage": "prospect",
        },
        {
            "id": "deal-2",
            "name": "Deal Two",
            "amount_usd": 250_000,
            "currency": "USD",
            "stage": "qualified",
        },
    ]
    assert pipeline_total(rows) == 350_000  # 100k + 250k, duplicate ignored


def test_closed_stage_ignored_but_open_duplicate_counts():
    rows = [
        {
            "id": "deal-3",
            "name": "Deal Three",
            "amount_usd": 500_000,
            "currency": "JPY",
            "stage": "closed_lost",  # should be ignored
        },
        {
            "id": "deal-3",  # same deal, open stage
            "name": "Deal Three",
            "amount_usd": 500_000,
            "currency": "JPY",
            "stage": "negotiation",
        },
        {
            "id": "deal-4",
            "name": "Deal Four",
            "amount_usd": 200_000,
            "currency": "CAD",
            "stage": "closed_won",  # ignored, no open counterpart
        },
    ]
    # Only the open row for deal-3 contributes
    assert pipeline_total(rows) == 500_000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", None]
                ),
            }
        ),
        min_size=0,
        max_size=30,
    )
)
def test_pipeline_total_is_not_greater_than_sum_of_open_rows(rows):
    total = pipeline_total(rows)
    open_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= open_sum
