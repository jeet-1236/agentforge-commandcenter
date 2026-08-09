from datetime import datetime


def hours_open(created_iso, now_iso):
    """Hours a support ticket has been open, from ISO-8601 timestamps that may carry timezone offsets."""
    # Parse the ISO timestamps, keeping any timezone information.
    created = datetime.fromisoformat(created_iso)
    now = datetime.fromisoformat(now_iso)

    # If a timestamp lacks timezone info, treat it as UTC.
    if created.tzinfo is None:
        from datetime import timezone
        created = created.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        from datetime import timezone
        now = now.replace(tzinfo=timezone.utc)

    # Compute the elapsed time in hours.
    return (now - created).total_seconds() / 3600.0
