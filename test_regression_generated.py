import pytest
from hypothesis import given, strategies as st

from commandcenter.pipeline import pipeline_total, OPEN_STAGES


def test_pipeline_total_dedupes_multi_currency():
    # Same deal appears twice with different currencies, both rows are open.
    rows = [
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 1_200_000,
            "currency": "EUR",
            "stage": "prospect",
        },
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 1_200_000,
            "currency": "GBP",
            "stage": "prospect",
        },
        {
            "id": "deal-2",
            "name": "Deal Two",
            "amount_usd": 800_000,
            "currency": "USD",
            "stage": "qualified",
        },
    ]
    # The total should count each distinct open deal once: 1_200_000 + 800_000
    assert pipeline_total(rows) == 2_000_000


def test_pipeline_total_excludes_closed_and_counts_once_per_id():
    rows = [
        {
            "id": "deal-1",
            "name": "Deal One",
            "amount_usd": 500_000,
            "currency": "USD",
            "stage": "closed_won",  # closed, should be ignored
        },
        {
            "id": "deal-2",
            "name": "Deal Two",
            "amount_usd": 300_000,
            "currency": "EUR",
            "stage": "negotiation",  # open
        },
        {
            "id": "deal-2",
            "name": "Deal Two",
            "amount_usd": 300_000,
            "currency": "GBP",
            "stage": "negotiation",  # duplicate open, should not double‑count
        },
        {
            "id": "deal-3",
            "name": "Deal Three",
            "amount_usd": 200_000,
            "currency": "USD",
            "stage": "closed_lost",  # closed, ignore
        },
    ]
    # Only deal-2 is open and counted once.
    assert pipeline_total(rows) == 300_000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "name": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
            }
        )
    )
)
def test_pipeline_total_matches_manual_implementation(rows):
    """Invariant: pipeline_total should equal a manual de‑duplication of open deals."""
    expected = 0
    seen_ids = set()
    for row in rows:
        if row["stage"] not in OPEN_STAGES:
            continue
        if row["id"] in seen_ids:
            continue
        expected += row["amount_usd"]
        seen_ids.add(row["id"])
    assert pipeline_total(rows) == expected
