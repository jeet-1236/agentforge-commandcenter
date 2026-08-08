import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    rows = [
        {"id": "d1", "name": "Deal1", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "d1", "name": "Deal1", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        {"id": "d2", "name": "Deal2", "amount_usd": 500, "currency": "USD", "stage": "qualified"},
        {"id": "d2", "name": "Deal2", "amount_usd": 500, "currency": "JPY", "stage": "qualified"},
        {"id": "d3", "name": "Deal3", "amount_usd": 200, "currency": "USD", "stage": "closed_won"},
    ]
    # Only the two distinct open deals should be counted.
    assert pipeline_total(rows) == 1000 + 500


def test_rows_without_id_are_ignored():
    rows = [
        {"name": "NoId", "amount_usd": 300, "currency": "USD", "stage": "prospect"},
        {"id": "d4", "name": "Deal4", "amount_usd": 400, "currency": "USD", "stage": "negotiation"},
    ]
    assert pipeline_total(rows) == 400


def test_is_open_respects_open_stages():
    for stage in OPEN_STAGES:
        assert is_open({"stage": stage}) is True
    assert is_open({"stage": "closed_won"}) is False
    assert is_open({}) is False


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(list(OPEN_STAGES)),
            }
        ),
        min_size=0,
        max_size=10,
    )
)
def test_pipeline_total_sum_of_unique_ids(rows):
    """When all rows are open and each deal id appears only once,
    pipeline_total should equal the simple sum of amount_usd."""
    # Ensure each id appears at most once – keep the first occurrence.
    seen = set()
    unique_rows = []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        unique_rows.append(r)

    expected = sum(r["amount_usd"] for r in unique_rows)
    assert pipeline_total(unique_rows) == expected
