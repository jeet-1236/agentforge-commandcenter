def sync_records(records, push):
    """
    Sync a list of `records` using the supplied `push` callable.

    Returns a dict with counts of successfully synced records and failed ones.
    """
    synced = 0
    failed = 0
    for record in records:
        try:
            push(record)
        except Exception:
            failed += 1
        else:
            synced += 1
    return {"synced": synced, "failed": failed}
