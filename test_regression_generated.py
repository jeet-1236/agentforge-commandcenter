import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open


def test_multi_currency_deal_counts_once():
    rows = [
        {
            "id": "D1",
            "name": "Deal 1",
            "amount_usd": 100,
            "currency": "EUR",
            "stage": "prospect",
        },
        {
            "id": "D1",
            "name": "Deal 1",
            "amount_usd": 100,
            "currency": "GBP",
            "stage": "prospect",
        },
        {
            "id": "D2",
            "name": "Deal 2",
            "amount_usd": 200,
            "currency": "USD",
            "stage": "qualified",
        },
    ]
    assert pipeline_total(rows) == 300


def test_closed_stage_is_ignored_and_not_deduped():
    rows = [
        {
            "id": "D1",
            "name": "Deal 1",
            "amount_usd": 150,
            "currency": "EUR",
            "stage": "closed_won",  # should be ignored
        },
        {
            "id": "D2",
            "name": "Deal 2",
            "amount_usd": 250,
            "currency": "USD",
            "stage": "negotiation",
        },
        {
            "id": "D2",
            "name": "Deal 2",
            "amount_usd": 250,
            "currency": "GBP",
            "stage": "negotiation",
        },
        {
            # missing id – should be skipped entirely
            "name": "Deal 3",
            "amount_usd": 300,
            "currency": "JPY",
            "stage": "prospect",
        },
    ]
    # D1 is closed, D2 appears twice but same id, missing-id row is skipped
    assert pipeline_total(rows) == 250


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.one_of(st.none(), st.text(min_size=1)),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
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
def test_pipeline_total_never_exceeds_sum_of_open_rows(rows):
    total = pipeline_total(rows)
    bound = sum(
        int(r["amount_usd"])
        for r in rows
        if is_open(r) and r.get("id") is not None
    )
    assert 0 <= total <= bound
