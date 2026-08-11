import pytest
from hypothesis import given, assume, strategies as st

from commandcenter.idempotency import charge


def test_charge_once_and_idempotent_behavior():
    ledger = {}
    request_id = "req-123"
    amount = 2500

    # First charge should increase balance
    first_balance = charge(ledger, request_id, amount)
    assert first_balance == amount
    assert ledger["balance_cents"] == amount
    assert request_id in ledger["applied"]

    # Second charge with same request_id should NOT change balance
    second_balance = charge(ledger, request_id, amount)
    assert second_balance == first_balance
    assert ledger["balance_cents"] == first_balance
    # applied list should not duplicate the request_id
    assert ledger["applied"].count(request_id) == 1


def test_charge_different_ids_accumulate():
    ledger = {}
    amount1 = 1000
    amount2 = 2000

    # Apply first request
    bal1 = charge(ledger, "req-A", amount1)
    assert bal1 == amount1

    # Apply a different request_id
    bal2 = charge(ledger, "req-B", amount2)
    assert bal2 == amount1 + amount2
    assert set(ledger["applied"]) == {"req-A", "req-B"}


@given(
    balance=st.integers(min_value=0, max_value=10_000),
    applied=st.lists(st.text(min_size=1), unique=True),
    amount=st.integers(min_value=0, max_value=10_000),
    new_id=st.text(min_size=1),
)
def test_charge_increments_balance_for_new_id(balance, applied, amount, new_id):
    assume(new_id not in applied)
    ledger = {"balance_cents": balance, "applied": list(applied)}
    original_balance = ledger["balance_cents"]

    new_balance = charge(ledger, new_id, amount)

    assert new_balance == original_balance + amount
    assert ledger["balance_cents"] == new_balance
    assert new_id in ledger["applied"]


@given(
    balance=st.integers(min_value=0, max_value=10_000),
    applied=st.lists(st.text(min_size=1), unique=True),
    amount=st.integers(min_value=0, max_value=10_000),
    repeated_id=st.text(min_size=1),
)
def test_charge_idempotent_multiple_calls_same_id(balance, applied, amount, repeated_id):
    assume(repeated_id not in applied)
    ledger = {"balance_cents": balance, "applied": list(applied)}

    first_balance = charge(ledger, repeated_id, amount)
    second_balance = charge(ledger, repeated_id, amount)

    # Second call must not change the balance
    assert second_balance == first_balance
    assert ledger["balance_cents"] == first_balance
    # request id appears exactly once
    assert ledger["applied"].count(repeated_id) == 1
