import re
import pytest
from commandcenter import theme

def test_status_ok_color_returns_brand_ok():
    assert theme.status_ok_color() == theme.BRAND_OK

def test_status_ok_color_is_expected_hex():
    color = theme.status_ok_color()
    assert isinstance(color, str)
    assert color == "#3fb950"
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", color) is not None

from hypothesis import given, strategies as st

@given(st.integers())
def test_status_ok_color_is_idempotent(_):
    first = theme.status_ok_color()
    second = theme.status_ok_color()
    assert first == second
    # also ensure the colour string satisfies basic hex colour constraints
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", first) is not None
