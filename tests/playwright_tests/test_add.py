import re

import pytest
from playwright.sync_api import expect

from tests.playwright_tests.test_delete import get_delete_button
from tests.testapp.views import FORMSET_PREFIX


@pytest.fixture
def add_row(formset):
    """Return the container for the add button."""
    return formset.locator(".add-row")


@pytest.fixture
def add_button(add_row):
    """Return the add button for the add row."""
    return add_row.locator(".add-btn")


@pytest.fixture
def new_form(forms, add_button):
    add_button.click()
    return forms.last


def test_adds_new_empty_form(add_button, forms):
    """Assert that clicking the 'add another' button adds a new empty form."""
    count = forms.count()
    add_button.click()
    expect(forms).to_have_count(count + 1)
    assert forms.count() == count + 1


def test_add_row_remains_last_div(add_row, add_button):
    """
    Assert that the add-row remains the last div in the formset after adding
    another form.
    """
    add_button.click()
    expect(add_row.locator("~ div")).to_have_count(0)


def test_new_form_inserted_after_last_form(forms, add_button):
    """Assert that the new form is inserted after the last form."""
    last_form = list(forms.all())[-1]
    expect(last_form.locator("~ .form-container")).to_have_count(0)
    add_button.click()
    expect(last_form.locator("~ .form-container")).to_have_count(1)


def test_add_updates_total_forms(management_total, add_button):
    """Assert that the management form is updated when adding new forms."""
    count = int(management_total.get_attribute("value"))
    add_button.click()
    assert int(management_total.get_attribute("value")) == count + 1


def test_new_form_ids_set(new_form, management_total):
    """Assert that the ids of the newly added elements are set."""
    count = int(management_total.get_attribute("value"))
    for element in new_form.locator("input").all():
        expect(element).to_have_id(re.compile(rf"^id_{FORMSET_PREFIX}-{count}"))


def test_new_form_names_set(new_form, management_total):
    """Assert that the names of the newly added elements are set."""
    count = int(management_total.get_attribute("value"))
    for element in new_form.locator("input").all():
        expect(element).to_have_attribute("name", re.compile(rf"^{FORMSET_PREFIX}-{count}"))


def test_new_form_labels_for_set(new_form, management_total):
    """Assert that the labels of the new form have their for attribute set."""
    count = int(management_total.get_attribute("value"))
    for element in new_form.locator("label").all():
        expect(element).to_have_attribute("for", re.compile(rf"^id_{FORMSET_PREFIX}-{count}"))


def test_new_form_delete_button(new_form):
    """Assert that the delete button works as expected."""
    btn = get_delete_button(new_form)
    btn.click()
    expect(new_form).to_have_class(re.compile("marked-for-removal"))
