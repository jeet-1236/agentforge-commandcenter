import pytest
from hypothesis import given, strategies as st

from commandcenter import theme


def test_status_ok_color_returns_brand_ok():
    """Regression test: the function must return the designated brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK
    # sanity check: it must not return the accent (blue) colour
    assert theme.status_ok_color() != theme.BRAND_ACCENT


@given(st.integers())
def test_status_ok_color_is_constant(_):
    """
    Property‑based test: for any input (which is ignored),
    the function should always return the same string.
    """
    result = theme.status_ok_color()
    assert isinstance(result, str)
    assert result == theme.BRAND_OK
    # calling it again yields the identical value
    assert theme.status_ok_color() == result
