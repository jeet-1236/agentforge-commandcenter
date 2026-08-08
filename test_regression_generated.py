import pytest
from hypothesis import given, strategies as st

import commandcenter.theme as theme


def test_status_ok_color_returns_brand_ok():
    # The function should return the defined brand‑ok colour.
    assert theme.status_ok_color() == theme.BRAND_OK
    # It should be a hex colour string of the expected form.
    assert isinstance(theme.status_ok_color(), str)
    assert theme.status_ok_color().startswith("#")
    assert len(theme.status_ok_color()) == 7


def test_status_ok_color_is_not_red():
    # Ensure the colour is not the typical red used for danger signals.
    assert theme.status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_is_constant(_):
    # No matter what unrelated input is generated, the function always returns the same constant.
    assert theme.status_ok_color() == theme.BRAND_OK
