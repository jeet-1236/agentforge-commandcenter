import re

import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import BRAND_OK, status_ok_color


def test_status_ok_color_returns_brand_ok():
    """Regression test checking the function returns the expected brand green."""
    assert status_ok_color() == BRAND_OK
    # Ensure it is not the generic red colour often used for errors.
    assert status_ok_color().lower() != "#ff0000"


def test_status_ok_color_is_hex_string():
    """Ensures the returned value looks like a valid 6‑digit hex colour."""
    colour = status_ok_color()
    assert isinstance(colour, str)
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", colour) is not None


@given(st.none())
def test_status_ok_color_is_idempotent(_):
    """Property‑based test: repeated calls yield the same result."""
    first = status_ok_color()
    second = status_ok_color()
    assert first == second
    # Additionally, the value remains a valid hex string on each call.
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", first) is not None
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", second) is not None
