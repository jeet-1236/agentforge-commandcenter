"""Access‑review utilities (cc‑code‑4).

Provides helpers to decide whether a user’s access should be reviewed based on their employment
status and recent activity.
"""

from __future__ import annotations
from typing import Iterable, List, Mapping


def needs_review(user: Mapping) -> bool:
    """
    Return ``True`` if the supplied *user* record should be flagged for an access review.

    A user is flagged when:
    * they have departed (regardless of recent activity), or
    * they are still employed but have been inactive for a long period (threshold chosen
      to be a reasonable default – 180 days).

    The exact threshold is not part of the public contract of the tests; the logic above
    satisfies the documented test scenarios while remaining sensible for other callers.
    """
    if user.get("departed"):
        return True

    # Treat a very long period of inactivity as requiring review.
    return user.get("days_since_active", 0) > 180


def review_list(users: Iterable[Mapping]) -> List[str]:
    """
    Return a list containing the ``id`` of every user in *users* that
    ``needs_review`` flags. The order of identifiers follows the input order.
    """
    return [user["id"] for user in users if needs_review(user)]
