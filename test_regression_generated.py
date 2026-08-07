import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK


def test_status_ok_color_returns_brand_ok():
    """Regression test for the fixed behaviour."""
    assert status_ok_color() == "#3fb950"
    assert status_ok_color() == BRAND_OK


def test_status_ok_color_is_valid_hex():
    """The colour token must be a 7‑character CSS hex string."""
    colour = status_ok_color()
    assert isinstance(colour, str)
    assert colour.startswith("#")
    assert len(colour) == 7
    # ensure all remaining characters are valid hex digits
    int(colour[1:], 16)  # will raise ValueError if not hex


@given(st.none())
def test_status_ok_color_is_constant(_):
    """Property‑based test: the function always returns the same constant."""
    assert status_ok_color() == BRAND_OK
    assert status_ok_color() == "#3fb950"
