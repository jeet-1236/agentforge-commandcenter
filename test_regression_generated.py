import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    rows = [
        {"id": "deal1", "name": "Deal One", "amount_usd": 100_000, "currency": "USD", "stage": "prospect"},
        {"id": "deal1", "name": "Deal One", "amount_usd": 100_000, "currency": "EUR", "stage": "prospect"},
        {"id": "deal2", "name": "Deal Two", "amount_usd": 250_000, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 350_000  # deal1 counted once + deal2


def test_closed_stages_are_excluded():
    rows = [
        {"id": "deal1", "name": "Deal One", "amount_usd": 120_000, "currency": "USD", "stage": "closed_won"},
        {"id": "deal2", "name": "Deal Two", "amount_usd": 80_000, "currency": "USD", "stage": "closed_lost"},
        {"id": "deal3", "name": "Deal Three", "amount_usd": 60_000, "currency": "USD", "stage": "proposal"},
        {"id": "deal3", "name": "Deal Three", "amount_usd": 60_000, "currency": "EUR", "stage": "proposal"},
    ]
    # Only deal3 is open and should be counted once
    assert pipeline_total(rows) == 60_000


def test_is_open_respects_open_stages():
    for stage in OPEN_STAGES:
        assert is_open({"stage": stage}) is True
    for stage in ("closed_won", "closed_lost", "archived"):
        assert is_open({"stage": stage}) is False


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "archived"]),
            }
        )
    )
)
def test_pipeline_total_never_exceeds_sum_of_all_open_rows(rows):
    total = pipeline_total(rows)
    # sum of amounts of all rows that are open (including duplicates)
    sum_open = sum(int(r["amount_usd"]) for r in rows if is_open(r))
    assert 0 <= total <= sum_open
