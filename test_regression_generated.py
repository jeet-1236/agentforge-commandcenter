import re

import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import BRAND_OK, status_ok_color, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    """Regression test: the healthy status colour must be the brand green."""
    assert status_ok_color() == BRAND_OK
    # Ensure it is not the accent colour (which would be a different brand colour)
    assert status_ok_color() != BRAND_ACCENT


def test_status_ok_color_is_valid_hex():
    """The colour string should be a valid 6‑digit hex colour starting with '#'."""
    colour = status_ok_color()
    assert isinstance(colour, str)
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", colour) is not None


@given(st.integers())
def test_status_ok_color_idempotent(_):
    """Calling the pure function any number of times yields the same value
    and that value satisfies the hex format."""
    first = status_ok_color()
    second = status_ok_color()
    assert first == second
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", first) is not None
