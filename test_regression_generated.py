import pytest
from commandcenter.theme import status_ok_color, BRAND_OK

def test_status_ok_color_returns_brand_ok():
    """Regression test: the function must return the brand green token."""
    assert status_ok_color() == "#3fb950"
    assert status_ok_color() == BRAND_OK

def test_status_ok_color_is_idempotent():
    """Calling the function repeatedly should always yield the same value."""
    first = status_ok_color()
    for _ in range(5):
        assert status_ok_color() == first

from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=1000))
def test_status_ok_color_invariant_repeat(_):
    """Property‑based: regardless of any external variation, the output never changes."""
    assert status_ok_color() == status_ok_color()
    assert isinstance(status_ok_color(), str)
    assert status_ok_color().startswith("#")
    assert len(status_ok_color()) == 7
    assert status_ok_color() == BRAND_OK
