import pytest
from hypothesis import given, strategies as st

from commandcenter.billing import line_total, invoice_total


def test_line_total_simple():
    assert line_total(199, 3) == 199 * 3
    assert line_total(0, 10) == 0
    assert line_total(250, 0) == 0


def test_invoice_total_matches_sum_of_lines():
    # Example with diverse prices and quantities
    lines = [(100, 2), (250, 1), (99, 5)]
    expected = sum(price * qty for price, qty in lines)
    assert invoice_total(lines) == expected

    # Single line invoice
    single = [(12345, 1)]
    assert invoice_total(single) == 12345

    # Empty invoice should be zero
    assert invoice_total([]) == 0


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=1_000_000),  # price in cents
            st.integers(min_value=0, max_value=10_000),   # quantity
        ),
        max_size=50,
    )
)
def test_invoice_total_is_sum_of_line_totals(lines):
    # The invariant: invoice_total must equal the sum of each line_total
    assert invoice_total(lines) == sum(line_total(p, q) for p, q in lines)
