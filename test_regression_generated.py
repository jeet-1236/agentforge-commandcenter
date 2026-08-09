import pytest
from commandcenter import pipeline
from hypothesis import given, strategies as st


def test_is_open_recognises_open_stages():
    for stage in pipeline.OPEN_STAGES:
        assert pipeline.is_open({"stage": stage}) is True
    assert pipeline.is_open({"stage": "closed_won"}) is False
    assert pipeline.is_open({"stage": "closed_lost"}) is False
    assert pipeline.is_open({}) is False


def test_pipeline_total_counts_each_deal_once_and_ignores_closed():
    rows = [
        {"id": "A", "name": "Deal A", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "A", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "B", "name": "Deal B", "amount_usd": "2000", "currency": "GBP", "stage": "qualified"},
        {"id": "C", "name": "Deal C", "amount_usd": 3000, "currency": "JPY", "stage": "closed_won"},
        {"id": "D", "name": "Deal D", "amount_usd": 4000, "currency": "CAD", "stage": "negotiation"},
        {"id": "D", "name": "Deal D", "amount_usd": 4000, "currency": "CHF", "stage": "negotiation"},
    ]
    # Expected: A (1000) + B (2000) + D (4000) = 7000
    assert pipeline.pipeline_total(rows) == 7000


def test_pipeline_total_handles_empty_and_all_closed():
    rows = [
        {"id": "X", "name": "Deal X", "amount_usd": 500, "currency": "USD", "stage": "closed_lost"},
        {"id": "Y", "name": "Deal Y", "amount_usd": 800, "currency": "EUR", "stage": "closed_won"},
    ]
    assert pipeline.pipeline_total(rows) == 0
    assert pipeline.pipeline_total([]) == 0


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.one_of(st.integers(min_value=0, max_value=10_000), st.integers(min_value=0, max_value=10_000).map(str)),
                "currency": st.text(min_size=3, max_size=3),
                "stage": st.sampled_from(list(pipeline.OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        )
    )
)
def test_pipeline_total_matches_manual_aggregation(rows):
    # Manual aggregation following the specification:
    manual = {}
    for r in rows:
        if r.get("stage") in pipeline.OPEN_STAGES:
            if r["id"] not in manual:
                manual[r["id"]] = int(r["amount_usd"])
    expected = sum(manual.values())
    assert pipeline.pipeline_total(rows) == expected
