"""commandcenter.ui_format — presentation helpers for the dashboard's KPI tiles.

These decide what a number LOOKS like on screen. Getting them wrong is a front-end defect: the underlying
data is perfectly correct, but the person reading the dashboard sees something unreadable. Formatting bugs
are among the most common front-end regressions precisely because every data test still passes.
"""
from __future__ import annotations


def money_short(amount_usd: int) -> str:
    """Money for a KPI tile.

    The rule the tiles use: a million or more is abbreviated to two decimals ("$1.84M"); anything smaller
    keeps its thousands separators ("$48,200"). The tile is ~90px wide, so a raw seven-digit number
    overflows its box and the reader sees a clipped, meaningless string.
    """
    return "$" + str(int(amount_usd))


def uptime_label(pct: float) -> str:
    """Uptime for a KPI tile, to two decimals: 99.4 -> '99.40%'."""
    return f"{pct:.2f}%"
