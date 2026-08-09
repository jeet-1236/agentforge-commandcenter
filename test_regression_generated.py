import pytest
from hypothesis import given, strategies as st

from commandcenter import pipeline


def make_row(deal_id: str, amount: int, stage: str) -> dict:
    """Helper to build a row dict matching the expected schema."""
    return {
        "id": deal_id,
        "name": f"Deal {deal_id}",
        "amount_usd": amount,
        "currency": "USD",
        "stage": stage,
    }


def test_pipeline_total_counts_each_deal_once():
    rows = [
        make_row("1", 100, "prospect"),      # open, first occurrence
        make_row("1", 100, "prospect"),      # same deal, duplicate currency – should be ignored
        make_row("2", 200, "closed_won"),    # closed – should be ignored
        make_row("3", 150, "negotiation"),   # open – should be counted
    ]
    # Only deals "1" and "3" are open and distinct
    assert pipeline.pipeline_total(rows) == 100 + 150


def test_pipeline_total_ignores_closed_and_counts_multiple_open_deals():
    rows = [
        make_row("a", 50, "qualified"),      # open
        make_row("b", 75, "closed_lost"),    # closed – ignored
        make_row("c", 25, "negotiation"),   # open
        make_row("a", 50, "qualified"),     # duplicate of "a" – ignored
    ]
    # Open distinct deals are "a" (50) and "c" (25)
    assert pipeline.pipeline_total(rows) == 75


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(
                    ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
                ),
            }
        ),
        min_size=0,
        max_size=20,
    )
)
def test_pipeline_total_idempotent(rows):
    """
    Duplicating the entire feed must not change the reported total,
    because each distinct open deal is counted at most once.
    """
    total_once = pipeline.pipeline_total(rows)
    total_twice = pipeline.pipeline_total(rows + rows)
    assert total_once == total_twice
    assert total_once >= 0  # totals are non‑negative integers.
