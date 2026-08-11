import pytest
from hypothesis import given, strategies as st

from commandcenter import billing


def test_line_total_basic():
    assert billing.line_total(199, 3) == 597  # 1.99 * 3 = 5.97 dollars -> 597 cents
    assert billing.line_total(0, 10) == 0
    assert billing.line_total(12345, 0) == 0


def test_invoice_total_examples():
    # Simple two-line invoice
    lines = [(199, 3), (250, 2)]  # 597 + 500 = 1097
    assert billing.invoice_total(lines) == 1097

    # Empty invoice
    assert billing.invoice_total([]) == 0

    # Multiple lines with varying quantities
    lines = [(100, 1), (200, 2), (300, 3)]  # 100 + 400 + 900 = 1400
    assert billing.invoice_total(lines) == 1400


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=1_000_000),  # price in cents
            st.integers(min_value=0, max_value=10_000)      # quantity
        ),
        max_size=50
    )
)
def test_invoice_total_matches_line_total_sum(lines):
    """Invariant: invoice_total equals the sum of the individual line_totals."""
    expected = sum(billing.line_total(price, qty) for price, qty in lines)
    assert billing.invoice_total(lines) == expected
