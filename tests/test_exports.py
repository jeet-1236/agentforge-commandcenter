from commandcenter.exports import truncate_name, export_row


def test_truncate_keeps_whole_characters_for_accented_names():
    # 10 CHARACTERS, not 10 bytes — an accented name must not be cut short
    assert truncate_name("José Álvarez", 10) == "José Álvar"


def test_truncate_leaves_short_names_untouched():
    assert truncate_name("Acme", 10) == "Acme"


def test_export_row_shape():
    assert export_row({"name": "Acme", "owner": "dana", "arr_usd": 1200}) == "Acme,dana,1200"
