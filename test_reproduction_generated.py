import pytest

from commandcenter.orders import order_total


def test_order_total_international_with_discount_and_tax():
    """
    An international order with a discount and tax should apply the tax to the discounted subtotal
    only once. For a $100.00 subtotal, 10% discount, and 20% VAT, the correct total is $108.00
    (9000 cents discounted subtotal + 1800 cents tax = 10800 cents).
    """
    subtotal_cents = 10_000      # $100.00
    discount_pct = 10.0         # 10% promo
    tax_pct = 20.0               # 20% VAT
    shipping_cents = 0           # no shipping

    assert order_total(subtotal_cents, discount_pct, tax_pct, shipping_cents) == 10_800  # $108.00
