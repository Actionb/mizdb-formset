from django import forms
from django.utils.translation import gettext


class FormsetDeletionWidget(forms.CheckboxInput):
    """Checkbox widget for the deletion of formset forms."""

    template_name = "mizdb_inlines/widgets/deletion_checkbox.html"

    def __init__(self, attrs=None, check_test=None):
        attrs = attrs or {}
        attrs["class"] = (attrs.get("class", "") + " d-none delete-cb").strip()
        if "title" not in attrs:
            attrs["title"] = gettext("Delete")
        super().__init__(attrs, check_test)

    class Media:
        css = {"all": ["mizdb_inlines/css/delete.css"]}
        js = ["mizdb_inlines/js/delete.js"]
