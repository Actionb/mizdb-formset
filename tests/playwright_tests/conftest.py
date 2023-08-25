import os
import re

import pytest

from django.urls import reverse

from tests.testapp.models import Contact, PhoneNumber


# https://github.com/microsoft/playwright-python/issues/439
# https://github.com/microsoft/playwright-pytest/issues/29#issuecomment-731515676
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def formset_page(page, live_server, contact_obj):
    page.goto(live_server.url + reverse("contact", args=[contact_obj.pk]))
    return page


@pytest.fixture
def contact_obj():
    return Contact.objects.create(first_name="Alice", last_name="Testman")


@pytest.fixture
def home_number(contact_obj):
    return PhoneNumber.objects.create(contact=contact_obj, label="Home", number="123456789")


@pytest.fixture
def work_number(contact_obj):
    return PhoneNumber.objects.create(contact=contact_obj, label="Work", number="987654321")


@pytest.fixture(autouse=True)
def test_data(contact_obj, home_number, work_number):
    return [contact_obj, home_number, work_number]


@pytest.fixture
def submit_button(formset_page):
    return formset_page.get_by_role("button", name=re.compile("save", re.IGNORECASE))


@pytest.fixture
def forms(formset_page):
    return formset_page.locator(".formset-container")


@pytest.fixture
def home_number_form(forms):
    return forms.first
