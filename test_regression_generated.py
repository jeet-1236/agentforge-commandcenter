import itertools

from commandcenter.pipeline import pipeline_total, OPEN_STAGES

from hypothesis import given, strategies as st


def remove_duplicate_ids(rows):
    """Return a list where only the first occurrence of each `id` is kept."""
    seen = set()
    result = []
    for r in rows:
        deal_id = r.get("id")
        if deal_id in seen:
            continue
        seen.add(deal_id)
        result.append(r)
    return result


def test_pipeline_total_counts_each_deal_once():
    rows = [
        {"id": "A", "stage": "prospect", "amount_usd": 1000, "currency": "EUR"},
        {"id": "A", "stage": "prospect", "amount_usd": 1000, "currency": "GBP"},
        {"id": "B", "stage": "closed_won", "amount_usd": 5000, "currency": "USD"},
        {"id": "C", "stage": "negotiation", "amount_usd": 2000, "currency": "JPY"},
    ]
    assert pipeline_total(rows) == 3000  # 1000 (A) + 2000 (C)


def test_pipeline_total_ignores_closed_and_respects_first_open():
    rows = [
        {"id": "D", "stage": "closed_lost", "amount_usd": 3000, "currency": "USD"},
        {"id": "D", "stage": "prospect", "amount_usd": 3000, "currency": "USD"},
    ]
    assert pipeline_total(rows) == 3000


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.text(min_size=1, max_size=5),
                "stage": st.sampled_from(
                    list(OPEN_STAGES) + ["closed_won", "closed_lost"]
                ),
                "amount_usd": st.integers(min_value=0, max_value=10_000),
                "currency": st.text(min_size=1, max_size=3),
            }
        ),
        max_size=20,
    )
)
def test_pipeline_total_is_idempotent_under_duplicate_removal(rows):
    # Removing duplicate ids (keeping the first occurrence) should not change the total.
    assert pipeline_total(rows) == pipeline_total(remove_duplicate_ids(rows))
