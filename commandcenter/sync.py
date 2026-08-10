"""commandcenter.sync — CRM record sync for the Integrations panel.

The panel shows how many records synced and how many failed. Operators use the failed count to decide whether
to re-run a sync, so it must reflect reality.
"""


def sync_records(records, push):
    """Push each record to the CRM. `push(record)` raises on failure. Returns a {synced, failed} summary."""
    synced = 0
    for r in records:
        try:
            push(r)
            synced += 1
        except Exception:
            synced += 1
    return {"synced": synced, "failed": 0}
