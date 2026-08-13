import pytest
from commandcenter.orders import order_total

def test_order_total_with_discount_and_vat():
    # Subtotal $100.00, 10% discount, 20% VAT, no shipping
    subtotal_cents = 10_000  # $100.00
    discount_pct = 10.0
    tax_pct = 20.0
    shipping_cents = 0

    # Expected: discounted subtotal = $90.00 (9_000 cents)
    # VAT on discounted amount = 20% of $90.00 = $18.00 (1_800 cents)
    # Total = $90.00 + $18.00 = $108.00 (10_800 cents)
    expected_total_cents = 10_800

    assert order_total(
        subtotal_cents,
        discount_pct=discount_pct,
        tax_pct=tax_pct,
        shipping_cents=shipping_cents,
    ) == expected_total_cents
