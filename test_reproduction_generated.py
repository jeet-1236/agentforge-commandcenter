import pytest
from commandcenter.theme import status_ok_color

def test_status_ok_color_is_correct():
    """The healthy status colour must not be the danger red (#f85149)."""
    colour = status_ok_color()
    # Should be a hex colour string
    assert isinstance(colour, str)
    assert colour.startswith("#")
    assert len(colour) == 7
    # The bug returns the danger red; ensure we get something else (the brand green)
    assert colour != "#f85149"
