import pytest
from commandcenter import billing

def test_invoice_total_basic_example():
    # 100 cents * 2 = 200, 250 cents * 3 = 750, total should be 950 cents
    lines = [(100, 2), (250, 3)]
    assert billing.invoice_total(lines) == 950
    # Verify that the sum of individual line_totals matches invoice_total
    assert billing.invoice_total(lines) == sum(billing.line_total(p, q) for p, q in lines)

def test_invoice_total_regression_one_cent_bug():
    # This set previously exposed the off‑by‑one bug.
    lines = [(1, 1), (2, 2), (3, 3)]  # expected total = 1*1 + 2*2 + 3*3 = 14
    expected = 14
    assert billing.invoice_total(lines) == expected
    # Ensure the result is not one cent short
    assert billing.invoice_total(lines) != expected - 1

from hypothesis import given, strategies as st

@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=10_000),  # price in cents
            st.integers(min_value=0, max_value=1_000)    # quantity
        ),
        max_size=20
    )
)
def test_invoice_total_consistent_with_line_total(lines):
    """invoice_total must equal the sum of the line_total for each (price, qty)."""
    total = billing.invoice_total(lines)
    expected = sum(billing.line_total(price, qty) for price, qty in lines)
    assert total == expected
