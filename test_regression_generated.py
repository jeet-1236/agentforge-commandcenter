import re

import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import (
    status_ok_color,
    BRAND_OK,
    BRAND_ACCENT,
)


def test_status_ok_color_returns_brand_ok():
    assert status_ok_color() == BRAND_OK
    assert status_ok_color() == "#3fb950"


def test_status_ok_color_is_not_accent():
    assert status_ok_color() != BRAND_ACCENT
    # Ensure it is not some generic red placeholder
    assert status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_idempotent(_):
    """The function is pure and deterministic; repeated calls give the same result."""
    first = status_ok_color()
    second = status_ok_color()
    assert first == second
    # Also verify the returned string looks like a hex colour code
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", first) is not None
