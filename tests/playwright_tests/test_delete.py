import re

import pytest
from playwright.sync_api import expect

from tests.testapp.views import FORMSET_PREFIX


def get_delete_button(form):
    return form.locator(".delete-btn")


@pytest.fixture
def first_form_delete_button(first_form):
    return get_delete_button(first_form)


@pytest.fixture
def reset_button(formset_page):
    """Return the form reset button."""
    return formset_page.get_by_role("button", name=re.compile("reset", re.IGNORECASE))


def test_can_delete(formset_page, first_form_delete_button, submit_button, home_number, contact_obj):
    """
    Assert that clicking on the 'delete' button and submitting the form deletes
    the form object.
    """
    first_form_delete_button.click()
    with formset_page.expect_request_finished():
        submit_button.click()
    assert home_number.pk not in contact_obj.phone_numbers.all()


def test_form_marked_for_removal(first_form_delete_button, first_form):
    """Assert that clicking the 'delete' button marks the form for removal."""
    first_form_delete_button.click()
    expect(first_form).to_have_class(re.compile(r"marked-for-removal"))


def test_form_disabled(first_form, first_form_delete_button):
    """Assert that clicking the 'delete' button disables the form controls."""
    first_form_delete_button.click()
    for elem in first_form.locator(".form-control").all():
        expect(elem).to_be_disabled()


def test_form_enabled(first_form, first_form_delete_button):
    """Assert that clicking the 'delete' button again enables the form controls."""
    first_form_delete_button.click()
    first_form_delete_button.click()
    for elem in first_form.locator(".form-control").all():
        expect(elem).to_be_enabled()


def test_empty_extra_forms_removed_from_dom(extra_forms):
    """
    Assert that extra forms that have no data are removed from the DOM instead
    of being marked.
    """
    count = extra_forms.count()
    btn = get_delete_button(extra_forms.first)
    btn.click()
    assert extra_forms.count() == count - 1


def test_bound_extra_forms_not_removed_from_dom(extra_forms):
    """Assert that extra forms that have data are not removed from the DOM."""
    extra_forms.first.get_by_label("Number").fill("192837465")
    count = extra_forms.count()
    btn = get_delete_button(extra_forms.first)
    btn.click()
    assert extra_forms.count() == count


def test_delete_updates_total_forms(extra_forms, management_total):
    """Assert that the management form is updated when removing forms from the DOM."""
    count = int(management_total.get_attribute("value"))
    btn = get_delete_button(extra_forms.first)
    btn.click()
    assert int(management_total.get_attribute("value")) == count - 1


def test_id_prefix_indices_updated_when_form_removed(extra_forms, management_total):
    """
    Assert that the prefix indices of following form control ids are updated
    when a previous form was removed from the DOM.
    """
    btn = get_delete_button(extra_forms.first)
    btn.click()
    index = int(management_total.get_attribute("value")) - 1
    for form in extra_forms.all():
        for element in form.locator("input,textarea,select").all():
            expect(element).to_have_attribute("id", re.compile(rf"^id_{FORMSET_PREFIX}-{index}"))


def test_name_prefix_indices_updated_when_form_removed(extra_forms, management_total):
    """
    Assert that the prefix indices of following form control names are updated
    when a previous form was removed from the DOM.
    """
    btn = get_delete_button(extra_forms.first)
    btn.click()
    index = int(management_total.get_attribute("value")) - 1
    for form in extra_forms.all():
        for element in form.locator("input,textarea,select").all():
            expect(element).to_have_attribute("name", re.compile(rf"^{FORMSET_PREFIX}-{index}"))


def test_label_prefix_indices_updated_when_form_removed(extra_forms, management_total):
    """
    Assert that the prefix indices of following form labels are updated when
    a previous form was removed from the DOM.
    """
    btn = get_delete_button(extra_forms.first)
    btn.click()
    index = int(management_total.get_attribute("value")) - 1
    for form in extra_forms.all():
        for element in form.locator("label").all():
            expect(element).to_have_attribute("for", re.compile(rf"^id_{FORMSET_PREFIX}-{index}"))


def test_reset_unmarks_form_for_removal(first_form, first_form_delete_button, reset_button):
    """Assert that clicking the reset button un-marks all forms."""
    first_form_delete_button.click()
    expect(first_form).to_have_class(re.compile(r"marked-for-removal"))
    reset_button.click()
    expect(first_form).not_to_have_class(re.compile(r"marked-for-removal"))


def test_reset_enables_forms(first_form, first_form_delete_button, reset_button):
    """Assert that clicking the reset button enables forms that were disabled."""
    first_form_delete_button.click()
    reset_button.click()
    for elem in first_form.locator(".form-controls").all():
        expect(elem).to_be_enabled()
