import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counted_once():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "deal-1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 2000, "currency": "USD", "stage": "qualified"},
    ]
    # Only deal-1 and deal-2 are open; deal-1 should be counted once despite two rows.
    assert pipeline_total(rows) == 3000


def test_closed_deals_are_ignored():
    rows = [
        {"id": "deal-1", "name": "Deal One", "amount_usd": 500, "currency": "USD", "stage": "closed_won"},
        {"id": "deal-2", "name": "Deal Two", "amount_usd": 1500, "currency": "USD", "stage": "closed_lost"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 2500, "currency": "USD", "stage": "proposal"},
        {"id": "deal-3", "name": "Deal Three", "amount_usd": 2500, "currency": "EUR", "stage": "proposal"},
    ]
    # Only deal-3 is open; its amount should be counted once.
    assert pipeline_total(rows) == 2500


def _expected_total(rows):
    total = 0
    seen = set()
    for r in rows:
        if r.get("stage") not in OPEN_STAGES:
            continue
        if r.get("id") in seen:
            continue
        seen.add(r.get("id"))
        total += int(r["amount_usd"])
    return total


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=10),
                "name": st.text(min_size=1, max_size=20),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", "archived"]
                ),
            },
            optional=None,
        ),
        min_size=0,
        max_size=50,
    )
)
def test_pipeline_total_matches_expected_logic(rows):
    assert pipeline_total(rows) == _expected_total(rows)
