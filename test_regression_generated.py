import pytest
from hypothesis import given, strategies as st

from commandcenter.billing import line_total, invoice_total


def test_line_total_basic():
    assert line_total(100, 3) == 300
    assert line_total(0, 5) == 0
    assert line_total(250, 0) == 0
    assert line_total(-100, 2) == -200  # confirm arithmetic is unchanged


def test_invoice_total_matches_manual_sum():
    lines = [(100, 2), (250, 1), (99, 3)]
    expected = sum(line_total(p, q) for p, q in lines)
    assert invoice_total(lines) == expected


def test_invoice_total_empty_iterable():
    assert invoice_total([]) == 0
    assert invoice_total(()) == 0
    assert invoice_total([]) == sum(line_total(p, q) for p, q in [])


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=10_000),  # price in cents
            st.integers(min_value=0, max_value=1_000)   # quantity
        ),
        max_size=20
    )
)
def test_invoice_total_is_sum_of_line_totals(lines):
    # Invariant: invoice_total equals the sum of each line_total
    assert invoice_total(lines) == sum(line_total(p, q) for p, q in lines)
