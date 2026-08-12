import pytest
from commandcenter import pipeline as cp


def test_pipeline_total_counts_each_deal_once(monkeypatch):
    # Force every row to be treated as an open deal
    monkeypatch.setattr(cp, "is_open", lambda row: True)

    rows = [
        {"id": 1, "amount_usd": "100000"},
        {"id": 1, "amount_usd": "100000"},  # same deal in another currency
        {"id": 2, "amount_usd": "50000"},
    ]

    # Expected total: each distinct deal counted once
    assert cp.pipeline_total(rows) == 150000  # 100k (deal 1) + 50k (deal 2)
