from commandcenter.ui_format import money_short, uptime_label


def test_kpi_money_is_compact_enough_to_fit_its_tile():
    # the KPI tile is ~90px wide: a raw seven-digit number overflows and renders unreadable
    assert money_short(1_840_000) == "$1.84M"
    assert money_short(48_200) == "$48.2k"
    assert money_short(950) == "$950"


def test_uptime_keeps_two_decimals():
    assert uptime_label(99.4) == "99.40%"
