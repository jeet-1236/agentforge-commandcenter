from commandcenter.idempotency import charge


def test_a_retried_request_does_not_charge_the_customer_twice():
    ledger = {}
    charge(ledger, "req-1", 2500)
    charge(ledger, "req-1", 2500)          # the client timed out and retried the SAME request
    assert ledger["balance_cents"] == 2500


def test_two_genuine_purchases_both_apply():
    ledger = {}
    charge(ledger, "req-1", 1000)
    charge(ledger, "req-2", 1500)
    assert ledger["balance_cents"] == 2500
