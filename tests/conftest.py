import pytest

from tests.testapp.models import Contact, PhoneNumber


@pytest.fixture
def contact_obj():
    return Contact.objects.create(first_name="Alice", last_name="Testman")


@pytest.fixture
def home_number(contact_obj):
    return PhoneNumber.objects.create(contact=contact_obj, label="Home", number="123456789")


@pytest.fixture
def work_number(contact_obj):
    return PhoneNumber.objects.create(contact=contact_obj, label="Work", number="987654321")


@pytest.fixture
def test_data(contact_obj, home_number, work_number):
    return [contact_obj, home_number, work_number]
