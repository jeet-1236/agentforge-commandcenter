import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "1", "name": "Deal A", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        {"id": "2", "name": "Deal B", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
        {"id": "3", "name": "Deal C", "amount_usd": 1500, "currency": "JPY", "stage": "closed_won"},
        {"id": "2", "name": "Deal B", "amount_usd": 2000, "currency": "CAD", "stage": "qualified"},
    ]
    # Only the first occurrence of each open deal should be counted.
    assert pipeline_total(rows) == 1000 + 2000


def test_closed_deals_are_ignored():
    rows = [
        {"id": "1", "name": "Deal A", "amount_usd": 500, "currency": "USD", "stage": "closed_lost"},
        {"id": "2", "name": "Deal B", "amount_usd": 800, "currency": "USD", "stage": "closed_won"},
        {"id": "3", "name": "Deal C", "amount_usd": 1200, "currency": "USD", "stage": "prospect"},
    ]
    # Only the open deal (id=3) should contribute.
    assert pipeline_total(rows) == 1200


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=3, max_size=3),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_matches_reference_implementation(rows):
    """
    For any feed of rows, the implemented `pipeline_total` must be equivalent to a
    straightforward reference implementation that applies the same open‑stage filter
    and de‑duplicates by deal id.
    """
    # Reference implementation mirroring the specification.
    def reference_total(data):
        seen = set()
        total = 0
        for r in data:
            if r["stage"] not in OPEN_STAGES:
                continue
            deal_id = r["id"]
            if deal_id in seen:
                continue
            seen.add(deal_id)
            total += int(r["amount_usd"])
        return total

    assert pipeline_total(rows) == reference_total(rows)
