import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    # The function should return the defined healthy brand colour.
    assert status_ok_color() == BRAND_OK
    # Basic sanity checks on the returned token.
    assert isinstance(status_ok_color(), str)
    assert status_ok_color().startswith("#")
    assert len(status_ok_color()) == 7


def test_status_ok_color_is_not_red():
    # Ensure the bug (returning a red colour) is not present.
    assert status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_is_idempotent(_):
    # Pure function: repeated calls must yield the same result.
    first = status_ok_color()
    second = status_ok_color()
    assert first == second
