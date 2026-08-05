"""commandcenter/theme.py — Command Center dashboard brand tokens.

The dashboard's primary accent (the SELECTED sidebar nav highlight, the logo tile, chart fills) is a single brand
token. Keeping the colour here — as one function, not scattered as CSS literals — is what lets a "wrong brand
colour" report be reproduced and fixed like any other code defect: one place to test, one place to change.
"""
from __future__ import annotations

BRAND_ACCENT = "#3b82f6"      # the Command Center brand blue (the dashboard --accent)


def nav_highlight_color() -> str:
    """The fill colour of the SELECTED sidebar nav item — the dashboard's primary "button" surface.

    KNOWN-ISSUE (cc-code-5): returns a muted grey instead of the brand accent, so the active nav item reads as
    disabled/greyed-out rather than highlighted. The fix returns BRAND_ACCENT so the selected item shows the brand
    colour again.
    """
    return "#6b7280"          # BUG: should be BRAND_ACCENT — a grey highlight reads as inactive
