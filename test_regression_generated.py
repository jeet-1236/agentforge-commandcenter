import pytest
from commandcenter import pipeline as p
from hypothesis import given, strategies as st


def make_row(deal_id: str, amount_usd: int, stage: str, currency: str) -> dict:
    return {
        "id": deal_id,
        "amount_usd": amount_usd,
        "stage": stage,
        "currency": currency,
        "name": f"Deal {deal_id}",
    }


def test_pipeline_total_counts_each_open_deal_once():
    rows = [
        make_row("D1", 100, "prospect", "EUR"),
        make_row("D1", 100, "prospect", "USD"),   # same deal, different currency
        make_row("D2", 250, "qualified", "GBP"),
        make_row("D3", 400, "closed_won", "JPY"),  # closed – should be ignored
        make_row("D2", 250, "qualified", "CAD"),  # duplicate open deal D2
    ]
    # Expected: D1 (100) + D2 (250) = 350
    assert p.pipeline_total(rows) == 350


def test_pipeline_total_ignores_closed_stages_and_handles_no_rows():
    rows = [
        make_row("A1", 150, "closed_lost", "USD"),
        make_row("A2", 300, "closed_won", "EUR"),
        make_row("A3", 0, "closed_won", "GBP"),
    ]
    # No open deals, total should be 0
    assert p.pipeline_total(rows) == 0

    # Empty input also yields 0
    assert p.pipeline_total([]) == 0


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1),
                "stage": st.sampled_from(
                    list(p.OPEN_STAGES) + ["closed_won", "closed_lost", "other"]
                ),
                "name": st.text(),
            }
        )
    )
)
def test_pipeline_total_invariant(rows):
    total = p.pipeline_total(rows)
    # total must be a non‑negative integer
    assert isinstance(total, int)
    assert total >= 0

    # total cannot exceed the sum of amounts from rows that are open
    sum_open = sum(int(r["amount_usd"]) for r in rows if p.is_open(r))
    assert total <= sum_open
