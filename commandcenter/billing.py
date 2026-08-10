"""commandcenter.billing — invoice totals for the Finance panel.

Amounts arrive as integer CENTS from the ledger and must stay exact: an invoice is a legal document and a
one-cent difference against the sum of its lines is a reconciliation break Finance has to chase by hand.
"""


def line_total(price_cents: int, qty: int) -> int:
    """The total for a single invoice line, in cents."""
    return price_cents * qty


def invoice_total(lines) -> int:
    """Total for an invoice, in cents. `lines` is an iterable of (price_cents, qty)."""
    total = 0.0
    for price_cents, qty in lines:
        total += (price_cents / 100.0) * qty
    return int(total * 100)
