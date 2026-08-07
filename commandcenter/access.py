"""Access‑review utilities (cc-code-4)."""

STALE_DAYS = 90  # dormant longer than this → flag for review


def needs_review(user: dict) -> bool:
    """Return True if the user should be included in the access‑review list.

    A user must be reviewed if they have departed, regardless of recent activity,
    or if they have been dormant longer than the stale‑days threshold.
    """
    departed = bool(user.get("departed", False))
    dormant = int(user.get("days_since_active", 0)) > STALE_DAYS
    return departed or dormant


def review_list(users: list[dict]) -> list[str]:
    """Collect the IDs of users that need an access review."""
    return [user["id"] for user in users if needs_review(user)]
