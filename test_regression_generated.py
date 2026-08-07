import re
import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK


def test_status_ok_color_returns_brand_ok():
    """Regression test: the function must return the brand's healthy green."""
    assert status_ok_color() == BRAND_OK
    # Ensure it is not the common danger‑red colour.
    assert status_ok_color() != "#ff0000"


def test_brand_ok_is_valid_hex_colour():
    """Regression test: the BRAND_OK constant should be a proper hex colour."""
    pattern = re.compile(r"^#[0-9a-fA-F]{6}$")
    assert pattern.match(BRAND_OK) is not None


@given(st.integers())
def test_status_ok_color_is_idempotent(_):
    """Property‑based test: repeated calls always yield the same valid colour."""
    colour = status_ok_color()
    # same on successive calls
    assert colour == status_ok_color()
    # still a valid hex colour
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", colour) is not None
