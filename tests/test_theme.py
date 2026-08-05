"""cc-code-5 — the dashboard's selected-nav highlight must be the brand accent, not a muted grey."""
from commandcenter import theme


def test_brand_accent_is_defined():
    # baseline (PASS_TO_PASS): the brand token itself is the Command Center blue
    assert theme.BRAND_ACCENT == "#3b82f6"


def test_nav_highlight_uses_brand_accent():
    # cc-code-5 REPRODUCTION TARGET: fails on the shipped grey, passes once the highlight returns the brand accent.
    assert theme.nav_highlight_color() == theme.BRAND_ACCENT, (
        f"nav highlight is {theme.nav_highlight_color()!r}, expected the brand accent {theme.BRAND_ACCENT!r}")
