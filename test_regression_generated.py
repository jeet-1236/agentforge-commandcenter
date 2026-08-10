import pytest
from hypothesis import given, strategies as st

from commandcenter.billing import line_total, invoice_total


def test_invoice_total_matches_sum_of_line_totals():
    lines = [(199, 2), (345, 1), (1234, 3)]
    expected = sum(line_total(p, q) for p, q in lines)
    assert invoice_total(lines) == expected


def test_invoice_total_with_empty_iterable():
    assert invoice_total([]) == 0
    assert invoice_total(()) == 0


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=1_000_000),
            st.integers(min_value=0, max_value=10_000),
        )
    )
)
def test_invoice_total_is_sum_of_line_totals_property(lines):
    """Invariant: invoice_total equals the sum of each line_total."""
    computed = invoice_total(lines)
    expected = sum(line_total(p, q) for p, q in lines)
    assert computed == expected
    assert computed >= 0
