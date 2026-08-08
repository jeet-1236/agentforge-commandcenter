import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT

def test_status_ok_color_returns_brand_ok():
    assert status_ok_color() == "#3fb950"
    assert status_ok_color() == BRAND_OK

def test_status_ok_color_is_not_brand_accent():
    assert status_ok_color() != "#3b82f6"
    assert status_ok_color() != BRAND_ACCENT

@given(st.integers())
def test_status_ok_color_is_constant(_):
    assert status_ok_color() == BRAND_OK
    assert status_ok_color() == status_ok_color()
