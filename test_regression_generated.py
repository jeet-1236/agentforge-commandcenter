import pytest
from hypothesis import given, strategies as st

import commandcenter.theme as theme


def test_status_ok_color_returns_brand_ok():
    """Regression test ensuring the function returns the brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK
    # The known green value should be "#3fb950"
    assert theme.status_ok_color() == "#3fb950"


def test_status_ok_color_is_consistent():
    """Calling the function multiple times should always yield the same result."""
    first = theme.status_ok_color()
    second = theme.status_ok_color()
    third = theme.status_ok_color()
    assert first == second == third


@given(st.integers())
def test_status_ok_color_is_valid_hex(_: int):
    """Property‑based test: the returned colour string is a proper 7‑character hex code."""
    colour = theme.status_ok_color()
    assert isinstance(colour, str)
    assert colour.startswith("#")
    assert len(colour) == 7
    # Ensure all non‑# characters are valid hexadecimal digits
    assert all(c in "0123456789abcdefABCDEF" for c in colour[1:])
