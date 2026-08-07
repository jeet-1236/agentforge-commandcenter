import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "deal1", "name": "Deal One", "amount_usd": 500_000, "currency": "USD", "stage": "prospect"},
        {"id": "deal1", "name": "Deal One", "amount_usd": 500_000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal2", "name": "Deal Two", "amount_usd": 300_000, "currency": "USD", "stage": "qualified"},
        {"id": "deal3", "name": "Deal Three", "amount_usd": 200_000, "currency": "GBP", "stage": "closed_won"},
    ]
    # deal1 appears twice (multi‑currency) but should be counted once.
    # deal3 is closed and should be ignored.
    assert pipeline_total(rows) == 500_000 + 300_000


def test_is_open_respects_open_stages_and_ignores_others():
    open_row = {"id": "1", "stage": "prospect"}
    closed_row = {"id": "2", "stage": "closed_lost"}
    unknown_row = {"id": "3", "stage": "archived"}
    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(unknown_row) is False


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "archived"]),
            }
        )
    )
)
def test_pipeline_total_never_exceeds_naive_open_sum(rows):
    """Because duplicate open deals are de‑duplicated, the total cannot exceed the naïve sum of all
    open rows' amounts."""
    naive_sum = sum(row["amount_usd"] for row in rows if row["stage"] in OPEN_STAGES)
    assert pipeline_total(rows) <= naive_sum
    assert pipeline_total(rows) >= 0
