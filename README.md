# mizdb-inlines
Django inline formsets with bootstrap for the MIZDB app.

Requires [django_bootstrap5](https://github.com/zostera/django-bootstrap5).

## Installation 
Install using pip:
```shell
pip install mizdb-inlines
```

Add to your `INSTALLED_APPS`:
```python
#settings.py
INSTALLED_APPS = [
    ...,
    "mizdb_inlines",
]
```

## Usage 
Use the `MIZInlineFormset` class as base for your formsets:
```python
formset = inlineformset_factory(formset=MIZInlineFormset, ...)
```

Render the formset using the `inline_formset` template tag from the `mizdb_inlines` template tag library:
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