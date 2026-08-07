import re

import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import BRAND_OK, status_ok_color


def test_status_ok_color_returns_brand_ok():
    """Regression test: healthy status colour must be the brand green."""
    result = status_ok_color()
    assert result == BRAND_OK
    assert isinstance(result, str)


def test_status_ok_color_is_valid_hex():
    """The colour token should be a 7‑character hex string (e.g. '#3fb950')."""
    result = status_ok_color()
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", result) is not None


@given(st.integers())
def test_status_ok_color_is_constant(_):
    """Property‑based test: the function returns the same constant regardless of any external input."""
    assert status_ok_color() == BRAND_OK
