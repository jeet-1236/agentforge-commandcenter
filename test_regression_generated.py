import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, OPEN_STAGES


def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "1", "name": "Deal1", "amount_usd": 100, "currency": "USD", "stage": "prospect"},
        {"id": "1", "name": "Deal1", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        {"id": "2", "name": "Deal2", "amount_usd": 200, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 300  # 100 + 200, duplicate id '1' counted once


def test_closed_deals_are_excluded_from_total():
    rows = [
        {"id": "1", "name": "Deal1", "amount_usd": 150, "currency": "USD", "stage": "closed_won"},
        {"id": "2", "name": "Deal2", "amount_usd": 250, "currency": "USD", "stage": "proposal"},
        {"id": "3", "name": "Deal3", "amount_usd": 300, "currency": "EUR", "stage": "closed_lost"},
    ]
    # Only the deal with stage 'proposal' should be counted
    assert pipeline_total(rows) == 250


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "JPY", "GBP"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "archived"]),
            }
        ),
        min_size=0,
        max_size=30,
    )
)
def test_pipeline_total_is_consistent_with_first_occurrence_logic(rows):
    """Invariant: the total equals the sum of amount_usd for the first occurrence of each
    open deal id (i.e., duplicates are ignored, closed stages are ignored)."""
    seen_ids = set()
    expected_total = 0
    for row in rows:
        if row["stage"] not in OPEN_STAGES:
            continue
        if row["id"] in seen_ids:
            continue
        seen_ids.add(row["id"])
        expected_total += row["amount_usd"]
    assert pipeline_total(rows) == expected_total
