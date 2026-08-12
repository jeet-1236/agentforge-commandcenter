import pytest
from commandcenter import contacts


def test_validate_contact_accepts_international_name_and_phone():
    contact = {
        "name": "Siobhán O'Brien",
        "phone": "+44 20 7946 0958",
    }
    errors = contacts.validate_contact(contact)
    assert errors == [], f"Expected no validation errors, got {errors}"
