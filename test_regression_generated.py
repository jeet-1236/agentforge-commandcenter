import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    """Regression test for the specific bug: status_ok_color must return the brand green."""
    assert status_ok_color() == BRAND_OK
    # Ensure the constant is the expected green value.
    assert BRAND_OK == "#3fb950"


def test_brand_accent_unchanged():
    """Sanity check that the brand accent token remains as defined."""
    assert BRAND_ACCENT == "#3b82f6"


@given(st.integers())
def test_status_ok_color_is_valid_hex(_):
    """Property‑based test: the colour string is always a valid 7‑character hex code."""
    colour = status_ok_color()
    assert isinstance(colour, str)
    assert colour.startswith("#")
    assert len(colour) == 7
    # All characters after the leading “#” must be hexadecimal digits.
    hex_part = colour[1:]
    assert all(c in "0123456789abcdefABCDEF" for c in hex_part)
