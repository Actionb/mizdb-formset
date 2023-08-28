from unittest import mock

import pytest
from bs4 import BeautifulSoup
from django import forms
from django.forms import formset_factory

from mizdb_inlines.renderers import DeletableFormRenderer, DeletableFormsetRenderer


class Form(forms.Form):
    foo = forms.CharField()
    bar = forms.CharField()


@pytest.fixture
def formset():
    return formset_factory(form=Form, can_delete=True, extra=1)()


@pytest.fixture
def form(formset):
    """Return a form for the form renderer."""
    return formset.forms[0]


@pytest.fixture
def prefixed_name(form, field_name):
    """Return the field name with the form prefix appended."""
    return form.add_prefix(field_name)


@pytest.fixture
def form_renderer(form):
    """Return a DeletableFormRenderer instance."""
    return DeletableFormRenderer(form)


@pytest.fixture
def formset_renderer(formset):
    return DeletableFormsetRenderer(formset)


@pytest.fixture
def rendered_form(form_renderer):
    """Render the form using form_renderer.render()."""
    return form_renderer.render()


@pytest.fixture
def form_html(rendered_form):
    """Return the HTML of the rendered form."""
    return BeautifulSoup(rendered_form, features="html.parser")


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
    """Return the HTML of the rendered fields."""
    return BeautifulSoup(rendered_fields, features="html.parser")


@pytest.fixture
def field_container(fields_html):
    """Return the container of the rendered fields."""
    return list(fields_html.children)[0]


@pytest.fixture
def delete_wrapper(fields_html):
    """Return the wrapper for the delete button."""
    return list(fields_html.children)[-1]


def test_form_renderer_adds_container(form_container):
    """Assert that the form rendered is surrounded by a container."""
    assert form_container


@pytest.mark.parametrize("css_class", ["row", "formset-container"])
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


@pytest.mark.parametrize("field_name", Form.base_fields)
def test_form_renderer_renders_form_fields(field_container, prefixed_name, field_name):
    """Assert that the form renderer renders the form fields."""
    assert field_container.find_all("input", type="text", attrs={"name": prefixed_name})


@pytest.mark.parametrize("field_name", ["DELETE"])
def test_form_renderer_renders_deletion_checkbox(
    fields_html, prefixed_name, field_name
):
    """Assert that the form renderer renders the deletion checkbox."""
    assert fields_html.find_all("input", type="checkbox", attrs={"name": prefixed_name})


@pytest.mark.parametrize("css_class", ["col", "formset-form"])
def test_field_container_css_classes(field_container, css_class):
    """Assert that the field container div contains the expected CSS classes."""
    assert css_class in field_container.attrs["class"]


@pytest.mark.parametrize("css_class", ["col-1", "delete-wrapper"])
def test_delete_wrapper_css_class(delete_wrapper, css_class):
    """Assert that the deletion wrapper div contains the expected CSS classes."""
    assert css_class in delete_wrapper.attrs["class"]


def test_formset_renderer_uses_own_form_renderer(formset_renderer):
    """
    Assert that the formset renderer renders the forms with the expected form
    renderer.
    """
    with mock.patch(
        "mizdb_inlines.renderers.DeletableFormRenderer.render"
    ) as render_mock:
        render_mock.return_value = ""
        formset_renderer.render()
    render_mock.asser_called()
