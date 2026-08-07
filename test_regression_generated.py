import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, is_open, OPEN_STAGES


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        {"id": "d1", "name": "Deal A", "amount_usd": 1000, "currency": "EUR", "stage": "prospect"},
        {"id": "d1", "name": "Deal A", "amount_usd": 1000, "currency": "GBP", "stage": "prospect"},
        {"id": "d2", "name": "Deal B", "amount_usd": 2000, "currency": "EUR", "stage": "qualified"},
        {"id": "d3", "name": "Deal C", "amount_usd": 1500, "currency": "USD", "stage": "closed_won"},
        {"id": "d4", "name": "Deal D", "amount_usd": 3000, "currency": "JPY", "stage": "proposal"},
        {"id": "d4", "name": "Deal D", "amount_usd": 3000, "currency": "CAD", "stage": "proposal"},
    ]
    # d1 appears twice (open), d2 appears once (open), d3 closed, d4 appears twice (open)
    # Expected total: 1000 (d1) + 2000 (d2) + 3000 (d4) = 6000
    assert pipeline_total(rows) == 6000


def test_pipeline_total_ignores_closed_stages_even_if_duplicate():
    rows = [
        {"id": "x1", "amount_usd": 500, "currency": "USD", "stage": "closed_lost"},
        {"id": "x1", "amount_usd": 500, "currency": "EUR", "stage": "closed_lost"},
        {"id": "x2", "amount_usd": 800, "currency": "USD", "stage": "negotiation"},
        {"id": "x2", "amount_usd": 800, "currency": "GBP", "stage": "closed_won"},
    ]
    # Only x2 with stage "negotiation" should be counted once.
    assert pipeline_total(rows) == 800


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]),
            },
            optional={"extra": st.none()},
        ),
        min_size=0,
        max_size=50,
    )
)
def test_pipeline_total_matches_first_open_occurrence_per_id(rows):
    """
    For any list of rows, pipeline_total should equal the sum of `amount_usd`
    of the first open row encountered for each distinct deal id.
    """
    total = pipeline_total(rows)

    seen = set()
    expected = 0
    for r in rows:
        if not is_open(r):
            continue
        deal_id = r.get("id")
        if deal_id in seen:
            continue
        seen.add(deal_id)
        expected += int(r["amount_usd"])

    assert total == expected
