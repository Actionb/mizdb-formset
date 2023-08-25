import re

import pytest
from playwright.sync_api import expect


def get_delete_button(form):
    return form.locator(".delete-btn")


@pytest.fixture
def home_number_form_delete_button(home_number_form):
    return get_delete_button(home_number_form)


def test_can_delete(formset_page, home_number_form_delete_button, submit_button, home_number, contact_obj):
    """
    Assert that clicking on the 'delete' button and submitting the form deletes
    the form object.
    """
    home_number_form_delete_button.click()
    with formset_page.expect_request_finished():
        submit_button.click()
    assert home_number.pk not in contact_obj.phone_numbers.all()


def test_form_marked_for_removal(home_number_form_delete_button, home_number_form):
    """Assert that clicking the 'delete' button marks the form for removal."""
    home_number_form_delete_button.click()
    expect(home_number_form).to_have_class(re.compile(r"marked-for-removal"))
