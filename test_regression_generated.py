import pytest
from hypothesis import given, strategies as st

import commandcenter.theme as theme


def test_status_ok_color_returns_brand_ok():
    """Regression test: healthy status colour must be the brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK


def test_status_ok_color_is_not_incorrect_red():
    """Ensures the fix didn't revert to the previous wrong behaviour."""
    wrong_red = "#ff0000"
    assert theme.status_ok_color() != wrong_red


@given(st.integers())
def test_status_ok_color_is_idempotent(_):
    """Property‑based test: repeated calls must yield the same colour."""
    assert theme.status_ok_color() == theme.status_ok_color()
