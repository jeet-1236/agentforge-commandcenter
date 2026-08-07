import pytest
from commandcenter import theme

def test_status_ok_color_returns_brand_ok():
    """Regression test: ensure the function returns the intended brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK
    assert theme.status_ok_color() == "#3fb950"


def test_status_ok_color_is_valid_hex():
    """The colour string should be a 7‑character hex code starting with '#'."""
    colour = theme.status_ok_color()
    assert isinstance(colour, str)
    assert colour.startswith("#")
    assert len(colour) == 7
    # Verify that the characters after '#' are valid hexadecimal digits
    int(colour[1:], 16)  # will raise ValueError if not hex


from hypothesis import given, strategies as st

@given(st.integers())
def test_status_ok_color_is_constant(_: int):
    """Property‑based test: regardless of any unrelated input, the function always returns BRAND_OK."""
    assert theme.status_ok_color() == theme.BRAND_OK
