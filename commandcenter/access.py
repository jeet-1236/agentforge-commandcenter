def review_list(employees):
    """The access-review list of flagged (departed) employee ids, for the printed report."""
    flagged = {e["id"] for e in employees if e.get("departed")}
    return list(flagged)
