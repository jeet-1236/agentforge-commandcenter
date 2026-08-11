import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_duplicate_open_deal_counted_once():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    # The duplicate for deal-1 should not inflate the total.
    assert pipeline_total(rows) == 3000


def test_closed_and_duplicate_mixed():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 500, "currency": "USD", "stage": "closed_won"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 500, "currency": "EUR", "stage": "closed_won"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 1500, "currency": "USD", "stage": "negotiation"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 800, "currency": "USD", "stage": "closed_lost"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 1500, "currency": "GBP", "stage": "negotiation"},
    ]
    # Only deal-2 is open and should be counted once.
    assert pipeline_total(rows) == 1500


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(min_size=1, max_size=10),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            }
        ),
        min_size=0,
        max_size=20,
    )
)
def test_pipeline_total_matches_manual_deduplication(rows):
    """
    For any feed, the pipeline total must equal the sum of `amount_usd`
    for each distinct deal id whose first **open** occurrence appears in the feed.
    """
    total = pipeline_total(rows)

    # Manual deduplication respecting the function's order of processing.
    seen = set()
    expected = 0
    for r in rows:
        if not is_open(r):
            continue
        deal_id = r.get("id")
        if deal_id is None or deal_id in seen:
            continue
        seen.add(deal_id)
        expected += int(r["amount_usd"])

    assert total == expected
