import pytest
from commandcenter.billing import line_total, invoice_total

def test_invoice_total_simple_example():
    lines = [(100, 2), (250, 1), (0, 5)]
    expected = 100 * 2 + 250 * 1 + 0 * 5
    assert invoice_total(lines) == expected

def test_invoice_total_empty():
    assert invoice_total([]) == 0

def test_line_total_matches_invoice_total_one_line():
    price, qty = 199, 3
    assert line_total(price, qty) == invoice_total([(price, qty)])

from hypothesis import given, strategies as st

@given(st.lists(st.tuples(st.integers(min_value=0, max_value=10_000),
                         st.integers(min_value=0, max_value=1_000))))
def test_invoice_total_is_sum_of_line_totals(lines):
    assert invoice_total(lines) == sum(line_total(p, q) for p, q in lines)
