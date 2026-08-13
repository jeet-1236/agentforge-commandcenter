import pytest
from commandcenter.orders import order_total

def test_international_order_with_promo_and_tax():
    """
    An international order with a subtotal of $100.00, a 10% promo code,
    and a 20% VAT should total $108.00 (10800 cents).
    The current buggy implementation undercharges.
    """
    subtotal_cents = 10_000  # $100.00
    discount_pct = 10.0      # 10% discount
    tax_pct = 20.0           # 20% VAT
    shipping_cents = 0

    expected_total_cents = 10_800  # $108.00
    assert order_total(subtotal_cents, discount_pct, tax_pct, shipping_cents) == expected_total_cents
