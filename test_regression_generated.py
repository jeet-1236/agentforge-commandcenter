import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_multi_currency_deal_counts_once():
    # Two rows for the same open deal (different currencies) should be counted once.
    rows = [
        {"id": "D1", "name": "Deal One", "amount_usd": 1000, "currency": "USD", "stage": "prospect"},
        {"id": "D1", "name": "Deal One", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        # A closed deal that appears twice should be ignored completely.
        {"id": "D2", "name": "Deal Two", "amount_usd": 500, "currency": "USD", "stage": "closed_won"},
        {"id": "D2", "name": "Deal Two", "amount_usd": 500, "currency": "EUR", "stage": "closed_won"},
        # Another open deal with a single currency row.
        {"id": "D3", "name": "Deal Three", "amount_usd": 250, "currency": "JPY", "stage": "negotiation"},
    ]
    assert pipeline_total(rows) == 1250  # 1000 (D1) + 250 (D3)


def test_is_open_respects_stage():
    open_row = {"id": "X", "stage": "qualified"}
    closed_row = {"id": "Y", "stage": "closed_lost"}
    missing_stage = {"id": "Z"}
    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(missing_stage) is False


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=1_000_000),
                "currency": st.sampled_from(["USD", "EUR", "JPY", "GBP"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost"]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_matches_reference_implementation(rows):
    """
    For any generated feed, the pipeline_total should equal the sum of each distinct
    open deal's amount_usd, counting each deal id exactly once.
    """
    # Reference implementation: keep first amount_usd seen for each open deal id.
    seen = {}
    for r in rows:
        if r.get("stage") not in OPEN_STAGES:
            continue
        deal_id = r.get("id")
        if deal_id not in seen:
            seen[deal_id] = int(r["amount_usd"])
    expected = sum(seen.values())
    assert pipeline_total(rows) == expected
