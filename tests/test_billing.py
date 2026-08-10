from commandcenter.billing import invoice_total, line_total


def test_line_total_is_exact():
    assert line_total(1999, 3) == 5997


def test_invoice_total_matches_the_sum_of_its_lines():
    # ten lines of $0.10 must total exactly $1.00 — Finance reconciles against this
    assert invoice_total([(10, 1)] * 10) == 100


def test_invoice_total_simple_case():
    assert invoice_total([(50, 2)]) == 100
