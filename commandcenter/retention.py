"""commandcenter.retention — data-retention sweep for the Compliance panel.

Records are kept for exactly `retention_days` and deleted on the day AFTER the window closes. Deleting early
is a compliance incident: the data was still inside its mandated retention period.
"""


def is_expired(age_days: int, retention_days: int) -> bool:
    """True when a record older than its retention window may be deleted."""
    return age_days >= retention_days


def expired_records(records, retention_days: int):
    return [r for r in records if is_expired(r["age_days"], retention_days)]
