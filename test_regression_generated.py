import pytest
from commandcenter.pipeline import pipeline_total, is_open

def test_multi_currency_open_deal_counts_once():
    rows = [
        {"id": "deal-1", "name": "Deal A", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal B", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    # Even though deal-1 appears twice (different currencies), it should be counted once.
    assert pipeline_total(rows) == 3000

def test_closed_deals_are_excluded_and_duplicates_ignored():
    rows = [
        {"id": "deal-1", "name": "Deal A", "amount_usd": 1500, "currency": "USD", "stage": "closed_won"},
        {"id": "deal-2", "name": "Deal B", "amount_usd": 2500, "currency": "USD", "stage": "proposal"},
        {"id": "deal-2", "name": "Deal B", "amount_usd": 2500, "currency": "JPY", "stage": "proposal"},
        {"id": "deal-3", "name": "Deal C", "amount_usd": 500,  "currency": "USD", "stage": "closed_lost"},
    ]
    # Only deal-2 is open; duplicate rows for deal-2 should be deduped.
    assert pipeline_total(rows) == 2500

# Property‑based test for the pure function pipeline_total
from hypothesis import given, strategies as st

@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "JPY", "GBP"]),
                "stage": st.sampled_from(
                    ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
                ),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_matches_manual_deduplication(rows):
    # manual implementation of the intended behavior
    total = 0
    seen = set()
    for r in rows:
        if r["stage"] not in ("prospect", "qualified", "proposal", "negotiation"):
            continue
        deal_id = r["id"]
        if deal_id in seen:
            continue
        seen.add(deal_id)
        total += r["amount_usd"]
    assert pipeline_total(rows) == total

def test_is_open_behaviour():
    open_row = {"stage": "proposal"}
    closed_row = {"stage": "closed_won"}
    missing_stage = {}
    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(missing_stage) is False
