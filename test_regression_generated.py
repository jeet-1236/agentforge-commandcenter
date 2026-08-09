import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "d1", "name": "Deal 1", "amount_usd": 100, "currency": "USD", "stage": "prospect"},
        {"id": "d1", "name": "Deal 1", "amount_usd": 100, "currency": "EUR", "stage": "prospect"},
        {"id": "d2", "name": "Deal 2", "amount_usd": 200, "currency": "GBP", "stage": "qualified"},
        {"id": "d3", "name": "Deal 3", "amount_usd": 150, "currency": "JPY", "stage": "closed_won"},
    ]
    # d1 appears twice (same amount_usd), d2 once, d3 is closed and should be ignored.
    assert pipeline_total(rows) == 300  # 100 (d1) + 200 (d2)


def test_is_open_respects_stage_set():
    open_row = {"id": "x", "stage": "proposal"}
    closed_row = {"id": "y", "stage": "closed_lost"}
    missing_stage_row = {"id": "z"}  # no stage key

    assert is_open(open_row) is True
    assert is_open(closed_row) is False
    assert is_open(missing_stage_row) is False
    # ensure that non‑open stages are exactly those not in OPEN_STAGES
    for stage in OPEN_STAGES:
        assert is_open({"id": "tmp", "stage": stage}) is True


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.sampled_from(["USD", "EUR", "GBP", "JPY", "CAD"]),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", None]),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_matches_manual_sum_for_unique_ids(rows):
    """
    For any list of rows where each `id` is unique, the total should equal the sum of
    `amount_usd` for rows whose stage is an open stage.
    """
    # Force unique ids
    unique_rows = []
    seen = set()
    for r in rows:
        if r["id"] not in seen:
            unique_rows.append(r)
            seen.add(r["id"])

    expected = sum(
        int(r["amount_usd"])
        for r in unique_rows
        if r.get("stage") in OPEN_STAGES
    )
    assert pipeline_total(unique_rows) == expected
