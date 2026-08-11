from commandcenter.ui_format import money_short, uptime_label


def test_kpi_money_is_compact_enough_to_fit_its_tile():
    # a million or more is abbreviated to two decimals; below that, thousands separators
    assert money_short(1_840_000) == "$1.84M"
    assert money_short(48_200) == "$48,200"
    assert money_short(950) == "$950"


def test_uptime_keeps_two_decimals():
    assert uptime_label(99.4) == "99.40%"
