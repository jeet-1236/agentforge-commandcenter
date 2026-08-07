import pytest
from commandcenter.theme import status_ok_color, BRAND_OK

def test_status_ok_color_returns_brand_ok():
    """Regression test: ensure the healthy status colour is the brand green."""
    assert status_ok_color() == BRAND_OK
    # The previous buggy implementation returned red; ensure we are not returning that.
    assert status_ok_color() != "#ff0000"

def test_status_ok_color_is_consistent():
    """The function should always return the same value on repeated calls."""
    first = status_ok_color()
    second = status_ok_color()
    assert first == second == BRAND_OK

from hypothesis import given, strategies as st

@given(st.integers())
def test_status_ok_color_idempotent(_):
    """Property‑based test: regardless of unrelated input, the colour stays constant."""
    assert status_ok_color() == BRAND_OK
    assert status_ok_color() == status_ok_color()
