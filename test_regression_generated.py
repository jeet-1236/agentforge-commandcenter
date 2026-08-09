import pytest
from commandcenter.paging import paginate

def test_paginate_middle_full_page():
    items = list(range(1, 21))  # 20 items
    per_page = 5
    page = 2  # should return items 6-10 (1-indexed)
    expected = [6, 7, 8, 9, 10]
    assert paginate(items, page, per_page) == expected
    assert len(paginate(items, page, per_page)) == per_page

def test_paginate_last_partial_page():
    items = list(range(1, 13))  # 12 items
    per_page = 5
    page = 3  # last page, only 2 items left (11,12)
    expected = [11, 12]
    assert paginate(items, page, per_page) == expected
    assert len(paginate(items, page, per_page)) == len(expected)

from hypothesis import given, strategies as st

@given(
    st.lists(st.integers()),
    st.integers(min_value=1, max_value=30),
    st.integers(min_value=1, max_value=30),
)
def test_paginate_hypothesis_consistency(items, per_page, page):
    start = (page - 1) * per_page
    expected = items[start:start + per_page]
    result = paginate(items, page, per_page)
    assert result == expected
    assert len(result) <= per_page
    # ensure result is a subsequence preserving order
    if result:
        assert result == [items[i] for i in range(start, min(start + per_page, len(items)))]
