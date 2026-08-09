from datetime import datetime


def hours_open(created_iso, now_iso):
    """Hours a support ticket has been open, from ISO-8601 timestamps that may carry timezone offsets."""
    created = datetime.fromisoformat(created_iso).replace(tzinfo=None)
    now = datetime.fromisoformat(now_iso).replace(tzinfo=None)
    return (now - created).total_seconds() / 3600.0
