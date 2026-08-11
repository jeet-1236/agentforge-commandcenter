import pytest
from hypothesis import given, strategies as st

from commandcenter.billing import line_total, invoice_total


def test_line_total_basic():
    # $1.99 * 2 = $3.98 => 398 cents
    assert line_total(199, 2) == 398


def test_invoice_total_multiple_lines():
    lines = [(100, 3), (250, 2), (99, 1)]
    expected = 100 * 3 + 250 * 2 + 99 * 1
    assert invoice_total(lines) == expected


def test_invoice_total_not_off_by_one():
    # Single cent line should total exactly one cent, not 0
    assert invoice_total([(1, 1)]) == 1


def test_invoice_total_empty():
    assert invoice_total([]) == 0


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=1_000_000),
            st.integers(min_value=0, max_value=10_000),
        ),
        max_size=20,
    )
)
def test_invoice_total_matches_sum_of_line_totals(lines):
    # The invoice total must equal the sum of the individual line totals
    assert invoice_total(lines) == sum(line_total(p, q) for p, q in lines)
