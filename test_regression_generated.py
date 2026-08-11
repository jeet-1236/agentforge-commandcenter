import re
import importlib

import pytest
from hypothesis import given, strategies as st

# Import the module under test
theme = importlib.import_module("commandcenter.theme")


def test_status_ok_color_returns_brand_ok():
    """Regression test: ensure the healthy status color is the brand green."""
    assert theme.status_ok_color() == theme.BRAND_OK
    # The brand green should be a valid hex colour string
    assert re.fullmatch(r"^#[0-9a-fA-F]{6}$", theme.BRAND_OK)


def test_status_ok_color_is_not_incorrect_red():
    """Regression test: the function must not return the previous incorrect red colour."""
    # The incorrect colour was presumably red; ensure it's not returned.
    assert theme.status_ok_color() != "#ff0000"


@given(st.integers())
def test_status_ok_color_is_consistent_and_valid(_):
    """
    Property‑based test: the function is pure, deterministic and always returns a valid hex colour.
    The input is ignored; the test is run many times to catch flaky behaviour.
    """
    colour = theme.status_ok_color()
    # Deterministic: repeated calls give the same result
    assert colour == theme.status_ok_color()
    # Valid hex colour format
    assert re.fullmatch(r"^#[0-9a-fA-F]{6}$", colour) is not None
    # Must equal the defined BRAND_OK constant
    assert colour == theme.BRAND_OK
