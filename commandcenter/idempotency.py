"""commandcenter.idempotency — charge de-duplication for the Billing surface.

A client that times out retries its request. Without an idempotency key the retry is indistinguishable from a
genuine second purchase, and the customer is charged twice — one of the most damaging and most common defects
in payment integrations.
"""
from __future__ import annotations


def charge(ledger: dict, request_id: str, amount_cents: int) -> int:
    """Apply a charge exactly once per `request_id`. Returns the ledger's new balance, in cents."""
    # If this request was already processed, return the existing balance without applying the charge again.
    if request_id in ledger.get("applied", []):
        return ledger.get("balance_cents", 0)

    ledger["balance_cents"] = ledger.get("balance_cents", 0) + int(amount_cents)
    ledger.setdefault("applied", []).append(request_id)
    return ledger["balance_cents"]
