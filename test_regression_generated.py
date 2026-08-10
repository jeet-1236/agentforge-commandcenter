import pytest
from commandcenter import theme
from hypothesis import given, strategies as st


def test_status_ok_color_returns_brand_ok():
    """Regression test: the function must return the brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK
    assert theme.status_ok_color() == "#3fb950"


def test_status_ok_color_is_not_red():
    """Ensure the bug (returning red) is not present."""
    assert theme.status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_is_constant(dummy):
    """Property‑based test: regardless of any input (none expected), the result is always the same constant."""
    assert theme.status_ok_color() == theme.BRAND_OK
