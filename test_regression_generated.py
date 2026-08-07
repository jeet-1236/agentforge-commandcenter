import pytest
from commandcenter import theme

def test_status_ok_color_returns_expected():
    # The function should return the brand's healthy green colour.
    assert theme.status_ok_color() == theme.BRAND_OK
    # Confirm the constant matches the documented hex value.
    assert theme.BRAND_OK == "#3fb950"

def test_status_ok_color_is_not_incorrect_red():
    # The previous buggy implementation returned a red colour; ensure that is no longer the case.
    assert theme.status_ok_color() != "#ff0000"
    # It also must not mistakenly return the accent blue.
    assert theme.status_ok_color() != theme.BRAND_ACCENT

from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=100))
def test_status_ok_color_idempotent(repetitions):
    # Repeated calls must always yield the same constant value.
    results = [theme.status_ok_color() for _ in range(repetitions + 1)]
    assert all(r == results[0] for r in results)
