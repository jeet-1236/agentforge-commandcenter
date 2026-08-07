import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_not_double_counted():
    rows = [
        {"id": "1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "1", "name": "Deal A", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        {"id": "2", "name": "Deal B", "amount_usd": 2000, "currency": "USD", "stage": "closed_won"},
        {"id": "3", "name": "Deal C", "amount_usd": 1500, "currency": "JPY", "stage": "qualified"},
    ]
    assert pipeline_total(rows) == 1000 + 1500


def test_rows_missing_id_are_skipped():
    rows = [
        {"id": None, "name": "X", "amount_usd": 500, "currency": "CAD", "stage": "prospect"},
        {"id": "4", "name": "Y", "amount_usd": 800, "currency": "USD", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 800


def test_duplicate_id_closed_stage_ignored():
    rows = [
        {"id": "5", "name": "Z", "amount_usd": 900, "currency": "AUD", "stage": "closed_lost"},
        {"id": "5", "name": "Z", "amount_usd": 900, "currency": "AUD", "stage": "prospect"},
    ]
    assert pipeline_total(rows) == 900


# ---- Property‑based test -----------------------------------------------------

row_strategy = st.fixed_dictionaries(
    {
        "id": st.one_of(st.none(), st.text(min_size=1)),
        "name": st.text(),
        "amount_usd": st.integers(min_value=0, max_value=10_000),
        "currency": st.text(min_size=1, max_size=3),
        "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]),
    }
)


@given(st.lists(row_strategy, max_size=30))
def test_pipeline_total_matches_expected(rows):
    def expected_total(rows_):
        seen = set()
        total = 0
        for r in rows_:
            if not is_open(r):
                continue
            deal_id = r.get("id")
            if deal_id is None or deal_id in seen:
                continue
            seen.add(deal_id)
            total += int(r["amount_usd"])
        return total

    assert pipeline_total(rows) == expected_total(rows)
