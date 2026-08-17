"""commandcenter.exports — CSV export for the Accounts panel.

Account names are free text and routinely contain accented or non-Latin characters (José, Müller, Ольга).
The export truncates long names to keep the column narrow.
"""

NAME_LIMIT = 10


def truncate_name(name: str, limit: int = NAME_LIMIT) -> str:
    """Shorten `name` to at most `limit` CHARACTERS for the export column."""
    return name.encode("utf-8")[:limit].decode("utf-8", errors="ignore")


def export_row(account: dict) -> str:
    return f"{truncate_name(account['name'])},{account['owner']},{account['arr_usd']}"
