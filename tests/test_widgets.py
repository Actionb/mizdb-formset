import pytest
from bs4 import BeautifulSoup

from mizdb_inlines.widgets import FormsetDeletionWidget


@pytest.fixture
def css_classes():
    """Return additional CSS classes for the widget."""
    return ""


@pytest.fixture
def widget_kwargs(css_classes):
    """Return additional keyword arguments for the widget."""
    if css_classes:
        return {"attrs": {"class": css_classes}}
    return {}


@pytest.fixture
def make_widget():
    """Return a factory function that creates a FormsetDeletionWidget."""

    def factory(**kwargs):
        return FormsetDeletionWidget(**kwargs)

    return factory


@pytest.fixture
def widget(make_widget, widget_kwargs):
    """Return a FormsetDeletionWidget instance."""
    return make_widget(**widget_kwargs)


@pytest.fixture
def rendered_widget(widget):
    """Render the widget and return the output."""
    return widget.render(name="DELETE", value=None)


@pytest.fixture
def widget_html(rendered_widget):
    """Return the HTML of the rendered widget."""
    return BeautifulSoup(rendered_widget, features="html.parser")


@pytest.fixture
def checkbox_input(widget_html):
    """Return the checkbox input of the rendered widget."""
    return widget_html.input


@pytest.fixture
def delete_button(widget_html):
    """Return the delete button of the rendered widget."""
    return widget_html.button


@pytest.mark.parametrize("css_classes", ["", "my-class"])
def test_init_adds_delete_classes(widget, css_classes):
    """Assert that the expected CSS classes are added during init."""
    expected_classes = " ".join(["d-none", "delete-cb"])
    if css_classes:
        assert widget.attrs["class"] == f"{css_classes} {expected_classes}"
    else:
        assert widget.attrs["class"] == expected_classes


def test_media_css(widget):
    """Assert that the required CSS is included in the widget's media."""
    assert "mizdb_inlines/css/delete.css" in widget.media._css["all"]


def test_media_js(widget):
    """Assert that the required Javascript is included in the widget's media."""
    assert "mizdb_inlines/js/delete.js" in widget.media._js


def test_render_includes_checkbox(checkbox_input):
    """Assert that the rendered widget includes the hidden checkbox input."""
    assert checkbox_input


def test_checkbox_is_hidden(checkbox_input):
    """Assert that the checkbox input is hidden."""
    assert "d-none" in checkbox_input.attrs["class"]


def test_checkbox_has_css_class(checkbox_input):
    """Assert that the checkbox input has the expected CSS class."""
    assert "delete-cb" in checkbox_input.attrs["class"]


def test_checkbox_name(checkbox_input):
    """Assert that the checkbox input has the expected name."""
    assert checkbox_input.attrs["name"] == "DELETE"


def test_render_includes_button(delete_button):
    """Assert that the rendered widget includes the delete button."""
    assert delete_button


def test_delete_button_css_class(delete_button):
    """Assert that the delete button has the expected CSS class."""
    assert "delete-btn" in delete_button.attrs["class"]


def test_delete_button_title(delete_button):
    """Assert that the delete button has the expected title."""
    assert delete_button.attrs["title"] == "Delete"
