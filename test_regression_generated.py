import pytest
from hypothesis import given, strategies as st

from commandcenter.theme import status_ok_color, BRAND_OK, BRAND_ACCENT


def test_status_ok_color_returns_brand_ok():
    """Regression test: healthy status colour should be the brand green."""
    assert status_ok_color() == BRAND_OK
    assert isinstance(status_ok_color(), str)


def test_brand_ok_constant_is_expected_hex():
    """Regression test: ensure the constant has the correct literal value."""
    assert BRAND_OK == "#3fb950"
    # also check the format of a hex colour token
    assert BRAND_OK.startswith("#")
    assert len(BRAND_OK) == 7
    # all characters after the hash should be valid hex digits
    int(BRAND_OK[1:], 16)  # will raise ValueError if not hex


@given(st.integers(min_value=0, max_value=20))
def test_status_ok_color_idempotent(repetitions):
    """
    Property‑based test: calling `status_ok_color` any number of times
    always yields the same result (pure, deterministic function).
    """
    first = status_ok_color()
    for _ in range(repetitions):
        assert status_ok_color() == first
    # also ensure the result remains equal to the constant
    assert first == BRAND_OK
