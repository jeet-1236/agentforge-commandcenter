import re

import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    assert status_ok_color() == BRAND_OK


def test_status_ok_color_is_not_incorrect_red():
    # The known incorrect colour (danger red) was never a valid brand token.
    # Ensure the function does not return it.
    assert status_ok_color() != "#ff0000"


def test_brand_ok_is_a_valid_hex_colour():
    assert isinstance(BRAND_OK, str)
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", BRAND_OK)


@given(st.integers())
def test_status_ok_color_is_valid_hex(_):
    color = status_ok_color()
    assert isinstance(color, str)
    assert len(color) == 7
    assert color.startswith("#")
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", color) is not None

def test_brand_accent_is_distinct_from_ok():
    # Ensure the two brand colours are not the same token.
    assert BRAND_ACCENT != BRAND_OK
    # Both should be valid hex colours.
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", BRAND_ACCENT) is not None
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", BRAND_OK) is not None
