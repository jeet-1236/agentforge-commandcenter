import pytest
from hypothesis import given, strategies as st

from commandcenter import theme


def test_status_ok_color_is_brand_ok():
    """Regression test: the function must return the brand green token."""
    assert theme.status_ok_color() == theme.BRAND_OK
    # Ensure the constant matches the expected hex format
    assert isinstance(theme.status_ok_color(), str)
    assert theme.status_ok_color().startswith("#")
    assert len(theme.status_ok_color()) == 7


@given(st.integers())
def test_status_ok_color_is_constant_for_any_input(_):
    """Property‑based test: the function is pure and returns the same value irrespective of external factors."""
    assert theme.status_ok_color() == theme.BRAND_OK
    # Repeated calls should be idempotent
    first = theme.status_ok_color()
    second = theme.status_ok_color()
    assert first == second
    assert first is second  # string interning makes them the same object in CPython
