import os
import re

import pytest
from django.urls import reverse

# https://github.com/microsoft/playwright-python/issues/439
# https://github.com/microsoft/playwright-pytest/issues/29#issuecomment-731515676
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def formset_page(page, live_server, contact_obj, test_data):
    page.goto(live_server.url + reverse("contact", args=[contact_obj.pk]))
    return page


@pytest.fixture
def submit_button(formset_page):
    """Return the form's submit button."""
    return formset_page.get_by_role("button", name=re.compile("save", re.IGNORECASE))


@pytest.fixture
def formset(formset_page):
    """Return the formset of the given page."""
    return formset_page.locator(".formset-container")


@pytest.fixture
def forms(formset):
    """Return the forms of the given formset."""
    return formset.locator("> .form-container")


@pytest.fixture
def home_number_form(forms):
    """Return the form with the 'Home' number."""
    return forms.first


@pytest.fixture
def management_total(formset):
    """Return the TOTAL_FORMS element of the management form."""
    return formset.locator("[id$=TOTAL_FORMS]")


@pytest.fixture
def extra_forms(formset):
    """Return all the extra forms."""
    return formset.locator("> .extra-form")
