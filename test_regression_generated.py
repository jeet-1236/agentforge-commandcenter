import random

import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open

def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "d1", "name": "Deal 1", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        {"id": "d1", "name": "Deal 1", "amount_usd": 100, "currency": "GBP", "stage": "prospect"},
        {"id": "d2", "name": "Deal 2", "amount_usd": 200, "currency": "USD", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 300

def test_pipeline_total_excludes_closed():
    rows = [
        {"id": "d1", "name": "Deal 1", "amount_usd": 100, "currency": "EUR", "stage": "closed_won"},
        {"id": "d2", "name": "Deal 2", "amount_usd": 200, "currency": "USD", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 200

def test_pipeline_total_mixed_stage_duplicate():
    rows = [
        {"id": "d1", "name": "Deal1", "amount_usd": 100, "currency": "EUR", "stage": "closed_lost"},
        {"id": "d1", "name": "Deal1", "amount_usd": 100, "currency": "GBP", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 100

row_strategy = st.fixed_dictionaries(
    {
        "id": st.text(min_size=1, max_size=5),
        "name": st.text(min_size=1, max_size=10),
        "amount_usd": st.integers(min_value=0, max_value=10_000),
        "currency": st.text(min_size=1, max_size=3),
        "stage": st.sampled_from(
            ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
        ),
    }
)

@given(rows=st.lists(row_strategy, max_size=20))
def test_pipeline_total_is_order_invariant(rows):
    shuffled = rows[:]
    random.shuffle(shuffled)
    assert pipeline_total(rows) == pipeline_total(shuffled)
