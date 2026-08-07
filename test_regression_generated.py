import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    """The function must return the brand's healthy green colour."""
    assert status_ok_color() == BRAND_OK
    # Ensure the return value matches the expected hex code.
    assert status_ok_color() == "#3fb950"


def test_status_ok_color_is_not_accent_or_wrong():
    """Healthy status colour should not be the brand accent (blue) or any other colour."""
    result = status_ok_color()
    assert result != BRAND_ACCENT
    assert result != "#ff0000"  # not red


@given(st.integers())  # input is irrelevant; we just repeat the call.
def test_status_ok_color_is_constant(_):
    """Calling the pure function repeatedly must always yield the same constant."""
    assert status_ok_color() == BRAND_OK
    assert status_ok_color() == status_ok_color()
