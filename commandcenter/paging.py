"""commandcenter.paging — slice a list of rows into fixed-size pages for the dashboard tables."""


def paginate(items, page, per_page):
    """Return the rows on `page` (1-indexed), `per_page` rows per page."""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]
