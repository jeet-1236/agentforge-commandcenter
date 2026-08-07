"""commandcenter.theme — brand and status colour tokens for the dashboard."""
from __future__ import annotations

# Brand colour tokens (hex strings)
BRAND_OK = "#3fb950"      # Command Center green – healthy status
BRAND_ACCENT = "#3b82f6"  # Command Center blue – accent colour

# Status colour tokens (could be overridden per status)
STATUS_OK = "#3fb950"     # healthy status colour – should match BRAND_OK
STATUS_WARN = "#d29922"   # warning colour
STATUS_ERR = "#d73a49"    # error colour


def status_ok_color() -> str:
    """
    Return the colour to use for a healthy (OK) status.

    Historically this returned the danger/red colour, which broke the visual
    contract for healthy signals. It should now return the brand green.
    """
    return BRAND_OK
