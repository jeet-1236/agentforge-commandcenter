import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_multi_currency_deal_is_not_double_counted():
    rows = [
        {
            "id": "deal-1",
            "name": "Acme Corp",
            "amount_usd": 250_000,
            "currency": "EUR",
            "stage": "prospect",
        },
        {
            "id": "deal-1",
            "name": "Acme Corp",
            "amount_usd": 250_000,
            "currency": "GBP",
            "stage": "prospect",
        },
        {
            "id": "deal-2",
            "name": "Beta LLC",
            "amount_usd": 400_000,
            "currency": "USD",
            "stage": "qualified",
        },
    ]
    # deal-1 appears twice but should only contribute once.
    assert pipeline_total(rows) == 250_000 + 400_000


def test_closed_stage_is_ignored_and_duplicates_handled():
    rows = [
        {
            "id": "d1",
            "name": "Alpha",
            "amount_usd": 100_000,
            "currency": "JPY",
            "stage": "closed_won",  # not open
        },
        {
            "id": "d2",
            "name": "Beta",
            "amount_usd": 150_000,
            "currency": "EUR",
            "stage": "qualified",
        },
        {
            "id": "d2",
            "name": "Beta",
            "amount_usd": 150_000,
            "currency": "USD",
            "stage": "qualified",
        },
        {
            "id": "d3",
            "name": "Gamma",
            "amount_usd": 200_000,
            "currency": "GBP",
            "stage": "negotiation",
        },
    ]
    # d1 is closed and ignored, d2 is duplicated, d3 is unique.
    assert pipeline_total(rows) == 150_000 + 200_000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=10),
                "name": st.text(min_size=1, max_size=15),
                "amount_usd": st.integers(min_value=0, max_value=10_000_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY", "CAD"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]),
            }
        ),
        min_size=0,
        max_size=50,
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_amounts(rows):
    """
    Because `pipeline_total` deduplicates by deal id, its result must never be larger than the
    naïve sum of `amount_usd` over all open rows.
    """
    naive_sum = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert pipeline_total(rows) <= naive_sum
    assert pipeline_total(rows) >= 0
