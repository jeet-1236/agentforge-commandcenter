import pytest
from hypothesis import given, strategies as st
from commandcenter import theme


def test_status_ok_color_returns_brand_ok():
    assert theme.status_ok_color() == "#3fb950"


def test_status_ok_color_is_not_incorrect_red():
    # The buggy implementation returned a red colour (commonly "#ff0000").
    # Ensure the fixed implementation does not return that value.
    assert theme.status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_is_constant(_: int):
    """The function is pure and deterministic: every call must return the same brand colour."""
    result = theme.status_ok_color()
    assert result == theme.BRAND_OK
    assert isinstance(result, str)
    assert result.startswith("#")
    assert len(result) == 7  # e.g., "#3fb950" length
