import itertools

import pytest
from hypothesis import given, strategies as st

from commandcenter import pipeline


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "deal-1", "stage": "prospect", "amount_usd": 250, "currency": "EUR"},
        {"id": "deal-1", "stage": "prospect", "amount_usd": 250, "currency": "GBP"},
        {"id": "deal-2", "stage": "qualified", "amount_usd": 400, "currency": "USD"},
        {"id": "deal-2", "stage": "qualified", "amount_usd": 400, "currency": "JPY"},
    ]
    # Both deals are open and appear twice (different currencies); each should be summed once.
    assert pipeline.pipeline_total(rows) == 250 + 400


def test_pipeline_total_ignores_closed_and_counts_open_once():
    rows = [
        {"id": "deal-1", "stage": "prospect", "amount_usd": 150, "currency": "EUR"},
        {"id": "deal-1", "stage": "prospect", "amount_usd": 150, "currency": "GBP"},
        {"id": "deal-2", "stage": "closed_won", "amount_usd": 300, "currency": "USD"},
        {"id": "deal-2", "stage": "closed_won", "amount_usd": 300, "currency": "JPY"},
        {"id": "deal-3", "stage": "negotiation", "amount_usd": 200, "currency": "CAD"},
    ]
    # deal-1 (open, duplicated) counted once, deal-3 (open, single) counted, deal-2 (closed) ignored.
    assert pipeline.pipeline_total(rows) == 150 + 200


@given(stage=st.sampled_from(pipeline.OPEN_STAGES))
def test_is_open_true_for_open_stages(stage):
    row = {"stage": stage}
    assert pipeline.is_open(row) is True


@given(
    stage=st.text()
    .filter(lambda s: s not in pipeline.OPEN_STAGES)
    .filter(lambda s: s)  # non‑empty
)
def test_is_open_false_for_other_stages(stage):
    row = {"stage": stage}
    assert pipeline.is_open(row) is False
