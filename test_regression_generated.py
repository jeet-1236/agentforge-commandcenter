import pytest
from hypothesis import given, strategies as st

# Example‑based regression tests
def test_status_ok_color_returns_brand_ok():
    from commandcenter.theme import status_ok_color, BRAND_OK
    assert status_ok_color() == BRAND_OK, "status_ok_color should return the brand green token"


def test_brand_ok_has_expected_hex_value():
    from commandcenter.theme import BRAND_OK
    assert BRAND_OK == "#3fb950", "BRAND_OK constant should match the expected green hex colour"


# Property‑based test for the pure function status_ok_color
@given(st.integers())  # input is ignored; we just want many executions
def test_status_ok_color_is_idempotent_and_well_formed(_):
    from commandcenter.theme import status_ok_color
    first = status_ok_color()
    second = status_ok_color()
    # Idempotence: repeated calls give the same result
    assert first == second
    # Invariant: result is a 7‑character hex colour string starting with '#'
    assert isinstance(first, str)
    assert first.startswith("#")
    assert len(first) == 7
    # All characters after the '#' should be valid hex digits
    hex_part = first[1:]
    assert all(c in "0123456789abcdefABCDEF" for c in hex_part)
