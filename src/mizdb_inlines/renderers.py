from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_bootstrap5.core import get_field_renderer
from django_bootstrap5.renderers import FormRenderer, FormsetRenderer


# FIXME: need a container/wrapper for the entire formset, so multiple formsets
#  can be used (and an add button can be assigned to each one)
# TODO: need to add an "empty" template?


class DeletableFormRenderer(FormRenderer):
    """
    Renderer for the forms of a formset that can be deleted.

    The form will be rendered with two columns; a wider column for all the
    fields and a narrower (col-1) column for the delete button.
    """

    def get_container_class(self):
        # FIXME: rename "formset-container": this isn't the container for the
        #  formset - just the form + delete
        return "row mb-1 align-items-center py-1 formset-container"

    def get_field_container_class(self):
        return "col formset-form"

    def get_delete_wrapper_class(self):
        return "col-1 delete-wrapper"

    def render(self):
        return format_html(
            '<div class="{container_class}">{form}</div>',
            container_class=self.get_container_class(),
            form=super().render(),
        )

    def render_fields(self):
        rendered_fields = rendered_delete = mark_safe("")
        kwargs = self.get_kwargs()
        renderer = get_field_renderer(**kwargs)
        for field in self.form:
            if field.name == DELETION_FIELD_NAME:
                # Render the widget without the label and without the wrapper:
                rendered_delete = renderer(field, **kwargs).get_field_html()
            else:
                rendered_fields += renderer(field, **kwargs).render()
        return format_html(
            '<div class="{field_container_class}">{fields}</div><div class="{delete_wrapper_class}">{delete}</div>',
            field_container_class=self.get_field_container_class(),
            fields=rendered_fields,
            delete_wrapper_class=self.get_delete_wrapper_class(),
            delete=rendered_delete,
        )


class DeletableFormsetRenderer(FormsetRenderer):
    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            rendered_forms += DeletableFormRenderer(form, **kwargs).render()
        return rendered_forms
