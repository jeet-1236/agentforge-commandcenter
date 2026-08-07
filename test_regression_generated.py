import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, OPEN_STAGES


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "deal1", "amount_usd": 100, "stage": "prospect"},
        {"id": "deal1", "amount_usd": 100, "stage": "prospect"},  # duplicate currency row
        {"id": "deal2", "amount_usd": 250, "stage": "qualified"},
        {"id": "deal3", "amount_usd": 400, "stage": "negotiation"},
        {"id": "deal3", "amount_usd": 400, "stage": "negotiation"},  # duplicate currency row
    ]
    # Expected total = 100 (deal1) + 250 (deal2) + 400 (deal3) = 750
    assert pipeline_total(rows) == 750


def test_pipeline_total_ignores_closed_deals():
    rows = [
        {"id": "deal1", "amount_usd": 500, "stage": "closed_won"},
        {"id": "deal1", "amount_usd": 500, "stage": "closed_won"},
        {"id": "deal2", "amount_usd": 300, "stage": "closed_lost"},
        {"id": "deal3", "amount_usd": 200, "stage": "negotiation"},
        {"id": "deal4", "amount_usd": 150, "stage": "prospect"},
    ]
    # Only deal3 and deal4 are open; total should be 200 + 150 = 350
    assert pipeline_total(rows) == 350


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        ),
        min_size=0,
    )
)
def test_pipeline_total_never_exceeds_sum_of_open_amounts(rows):
    """
    For any list of rows, the pipeline total should never be larger than the
    sum of the amounts of rows that are in an open stage, because the function
    de‑duplicates deals and skips closed ones.
    """
    total = pipeline_total(rows)
    open_sum = sum(r["amount_usd"] for r in rows if r["stage"] in OPEN_STAGES)
    assert total <= open_sum
