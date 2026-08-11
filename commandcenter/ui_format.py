"""commandcenter.ui_format — presentation helpers for the dashboard's KPI tiles.

These decide what a number LOOKS like on screen. Getting them wrong is a front-end defect: the underlying
data is perfectly correct, but the person reading the dashboard sees something unreadable. Formatting bugs
are among the most common front-end regressions precisely because every data test still passes.
"""
from __future__ import annotations


def money_short(amount_usd: int) -> str:
    """Compact money for a KPI tile: 1_840_000 -> '$1.84M', 48_200 -> '$48.2k', 950 -> '$950'.

    The tile is ~90px wide, so a raw seven-digit number overflows its box and the reader sees a clipped,
    meaningless string where the pipeline value should be.
    """
    return "$" + str(int(amount_usd))


def uptime_label(pct: float) -> str:
    """Uptime for a KPI tile, to two decimals: 99.4 -> '99.40%'."""
    return f"{pct:.2f}%"
