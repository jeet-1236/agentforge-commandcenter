import pytest
from hypothesis import given, strategies as st

from commandcenter.billing import line_total, invoice_total


def test_invoice_total_basic_example():
    lines = [(100, 2), (250, 3), (0, 5)]
    expected = sum(price * qty for price, qty in lines)
    assert invoice_total(lines) == expected
    # individual line_total correctness
    for price, qty in lines:
        assert line_total(price, qty) == price * qty


def test_invoice_total_edge_cases():
    # empty invoice
    assert invoice_total([]) == 0
    # zero quantity and zero price
    lines = [(0, 0), (12345, 0), (0, 7)]
    expected = sum(price * qty for price, qty in lines)
    assert invoice_total(lines) == expected
    # negative values (if allowed by upstream validation)
    lines = [(-100, 2), (200, -3), (-50, -4)]
    expected = sum(price * qty for price, qty in lines)
    assert invoice_total(lines) == expected


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=10_000),  # price_cents
            st.integers(min_value=0, max_value=1_000)   # qty
        )
    )
)
def test_invoice_total_matches_sum_of_line_totals(lines):
    # Invariant: invoice_total equals the sum of each line_total
    assert invoice_total(lines) == sum(line_total(p, q) for p, q in lines)
