# mizdb-inlines

Django inline formsets with bootstrap for the MIZDB app.

Requires [django_bootstrap5](https://github.com/zostera/django-bootstrap5).

Formsets will be rendered in a layout with two columns. One column is for the formset
form, and the other column is for the delete button (or checkbox) of a given formset form.

Included is a `FormsetDeletionWidget` widget that can be used as the `deletion_widget` for the formset class.
The widget replaces the delete checkbox with a delete button. The button marks a form for removal and disables it.

## Installation

Install using pip:

```shell
pip install mizdb-inlines
```

Add to your `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    "mizdb_inlines",
]
```

## Usage

To make use of the `FormsetDeletionWidget`, either set the `deletion_widget` on your formset class:

```python
from mizdb_inlines.widgets import FormsetDeletionWidget


class MyFormset(forms.BaseInlineFormSet):
    deletion_widget = FormsetDeletionWidget
```

Or use the `MIZInlineFormset` class as base for your formsets:

```python
from mizdb_inlines.forms import MIZInlineFormset

formset = inlineformset_factory(formset=MIZInlineFormset, ...)
```

Then render the formset using the `inline_formset` template tag from the `mizdb_inlines` template tag library:

```html
<!DOCTYPE html>
{% load mizdb_inlines django_bootstrap5 %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Awesome Form</title>
    {{ form.media }}
    {{ formset.media }}
    {% bootstrap_css %}
    {% bootstrap_javascript %}
</head>
<body>
<form class="container mt-3" method="post">
    {% csrf_token %}

    {% bootstrap_form form %}
    {% inline_formset formset layout="horizontal" %}
    {% bootstrap_button button_type="submit" button_class="success" content="Save" %}
    {% bootstrap_button button_type="reset" button_class="warning" content="Reset" %}
</form>
</body>
</html>
```

## Development & Demo

```bash
python3 -m venv venv
source venv/bin/activate
make init
```

See the demo for a preview: run `make init-demo` and then start the demo server `python demo/manage.py runserver`.

Run tests with `make test`. To install required browsers for playwright: `playwright install`.