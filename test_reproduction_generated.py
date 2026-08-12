import pytest
from commandcenter.orders import order_total

def test_order_total_applies_tax_to_discounted_subtotal():
    """
    An international order with a promotional discount and VAT should calculate tax on the
    discounted subtotal, not on the discount a second time.
    """
    subtotal_cents = 10_000      # $100.00
    discount_pct = 10.0         # 10% promo
    tax_pct = 20.0              # 20% VAT
    shipping_cents = 0

    # Expected: 10% off => $90.00 (9_000 cents)
    # VAT on $90.00 => $18.00 (1_800 cents)
    # Total => $108.00 (10_800 cents)
    expected_total_cents = 10_800

    assert order_total(
        subtotal_cents,
        discount_pct=discount_pct,
        tax_pct=tax_pct,
        shipping_cents=shipping_cents,
    ) == expected_total_cents, "Tax should be calculated on the discounted subtotal, not on a double‑discounted amount"
