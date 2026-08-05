import pytest
from hypothesis import given, strategies as st
from commandcenter import theme


def test_status_ok_color_returns_brand_ok():
    """Regression test for the bug where the healthy colour was red."""
    # The function should return the defined brand green.
    assert theme.status_ok_color() == theme.BRAND_OK
    # Verify the exact expected hex value.
    assert theme.status_ok_color() == "#3fb950"


def test_status_ok_color_is_not_red():
    """Ensure the colour is not the red used for danger states."""
    # A typical danger red (not defined in the module) must not be returned.
    assert theme.status_ok_color() != "#d73a49"


@given(st.integers(min_value=0, max_value=1000))
def test_status_ok_color_is_idempotent(call_count):
    """Property‑based test: calling the pure function any number of times
    always yields the same brand‑green colour."""
    results = [theme.status_ok_color() for _ in range(call_count)]
    assert all(color == theme.BRAND_OK for color in results)
