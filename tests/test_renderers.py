from unittest import mock

import pytest
from bs4 import BeautifulSoup
from django.forms import inlineformset_factory

from mizdb_inlines.renderers import InlineFormRenderer, InlineFormsetRenderer
from tests.testapp.models import Contact, PhoneNumber

FORMSET_PREFIX = "foo_bar"
FORMSET_FIELDS = ["label", "number"]

pytestmark = [pytest.mark.django_db]


def get_formset_class(**kwargs):
    defaults = {"fields": FORMSET_FIELDS, "extra": 1}
    return inlineformset_factory(Contact, PhoneNumber, **{**defaults, **kwargs})


def get_formset_renderer(formset):
    """Return a FormRenderer instance for the given formset."""
    return InlineFormsetRenderer(formset)


def get_form_renderer(form):
    """Return a InlineFormRenderer instance for the given form."""
    return InlineFormRenderer(form)


@pytest.fixture
def formset(contact_obj):
    """Return a Django formset instance."""
    return get_formset_class()(instance=contact_obj, prefix=FORMSET_PREFIX)


@pytest.fixture
def formset_renderer(formset):
    """Return a FormRenderer instance for the default test formset."""
    return get_formset_renderer(formset)


@pytest.fixture
def rendered_formset(formset_renderer):
    """Render a formset using formset_renderer.render()."""
    return formset_renderer.render()


@pytest.fixture
def formset_html(rendered_formset):
    """Return the HTML of the rendered formset."""
    return BeautifulSoup(rendered_formset, features="html.parser")


@pytest.fixture
def formset_container(formset_html):
    """Return the div that wraps the formset."""
    return formset_html.div


@pytest.fixture
def formset_form_containers(formset_html):
    """Return the divs that wrap the formset forms."""
    return formset_html.find_all("div", class_="form-container")


@pytest.fixture
def form(formset):
    """Return a formset form for the form renderer."""
    # Note that the form has had the DELETE field added by Formset.add_fields
    return formset.forms[0]


@pytest.fixture
def form_renderer(form):
    """Return a InlineFormRenderer instance for the default test form."""
    return get_form_renderer(form)


@pytest.fixture
def rendered_form(form_renderer):
    """Render a form using form_renderer.render()."""
    return form_renderer.render()


@pytest.fixture
def form_html(rendered_form):
    """Return the HTML of the rendered form."""
    return BeautifulSoup(rendered_form, features="html.parser")


@pytest.fixture
def prefixed_name(form, field_name):
    """Return the field name with the form prefix appended."""
    return form.add_prefix(field_name)


@pytest.fixture
def form_container(form_html):
    """Return the container of the rendered form."""
    return form_html.div


@pytest.fixture
def rendered_fields(form_renderer):
    """Render the form fields using form_renderer.render_fields()."""
    return form_renderer.render_fields()


@pytest.fixture
def fields_html(rendered_fields):
    """Return the HTML of the rendered form fields."""
    return BeautifulSoup(rendered_fields, features="html.parser")


@pytest.fixture
def field_container(fields_html):
    """Return the container of the rendered fields."""
    return list(fields_html.children)[0]


@pytest.fixture
def delete_wrapper(fields_html):
    """Return the wrapper for the delete button."""
    return list(fields_html.children)[-1]


@pytest.fixture
def empty_form(formset_form_containers):
    """Return the empty form template."""
    return formset_form_containers[-1]


@pytest.fixture
def extra_form(formset_form_containers):
    """Return the extra form."""
    return formset_form_containers[-2]


@pytest.mark.parametrize("css_class", ["row", "form-container"])
def test_form_container_css_classes(form_container, css_class):
    """Assert that the form container has the expected CSS classes."""
    assert css_class in form_container.attrs["class"]


def test_fields_rendered_as_two_divs(fields_html):
    """
    Assert that the form renderer renders the formset forms with two divs;
    one for the form and one for the deletion button.
    """
    assert len(fields_html.contents) == 2
    assert all(e.name == "div" for e in fields_html.contents)


@pytest.mark.parametrize("field_name", FORMSET_FIELDS)
def test_form_fields_rendered(field_container, prefixed_name, field_name):
    """Assert that the form renderer renders the form fields."""
    assert field_container.find_all("input", type="text", attrs={"name": prefixed_name})


@pytest.mark.parametrize("field_name", ["DELETE"])
def test_deletion_checkbox_rendered(fields_html, prefixed_name, field_name):
    """Assert that the form renderer renders the deletion checkbox."""
    assert fields_html.find_all("input", type="checkbox", attrs={"name": prefixed_name})


@pytest.mark.parametrize("css_class", ["col", "fields-container"])
def test_field_container_css_classes(field_container, css_class):
    """Assert that the field container div contains the expected CSS classes."""
    assert css_class in field_container.attrs["class"]


@pytest.mark.parametrize("css_class", ["col-1", "delete-container"])
def test_delete_wrapper_css_class(delete_wrapper, css_class):
    """Assert that the deletion wrapper div contains the expected CSS classes."""
    assert css_class in delete_wrapper.attrs["class"]


def test_formset_renderer_uses_own_form_renderer(formset_renderer):
    """
    Assert that the formset renderer renders the forms with the expected form
    renderer.
    """
    with mock.patch("mizdb_inlines.renderers.InlineFormRenderer.render") as render_mock:
        render_mock.return_value = ""
        formset_renderer.render()
    render_mock.asser_called()


@pytest.mark.parametrize("css_class", ["formset-container", FORMSET_PREFIX])
def test_formset_container_css_class(formset_container, css_class):
    """Assert that the formset container contains the expected CSS classes."""
    assert css_class in formset_container.attrs["class"]


def test_formset_includes_add_button(formset_html):
    """Assert that the formset includes an 'add another' button."""
    assert formset_html.find_all("button", class_="add-btn")


def test_formset_includes_form_template(formset_html):
    """Assert that the formset includes an empty form template."""
    assert formset_html.find_all("div", class_="empty-form")


def test_extra_form_has_extra_class(extra_form):
    """Assert that the extra forms have the expected CSS class."""
    assert "extra-form" in extra_form.attrs["class"]


def test_form_template_has_extra_class(empty_form):
    """Assert that the empty form template has the expected CSS class."""
    assert "extra-form" in empty_form.attrs["class"]
