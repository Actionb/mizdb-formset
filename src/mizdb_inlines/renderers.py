from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_bootstrap5.core import get_field_renderer
from django_bootstrap5.renderers import FormRenderer, FormsetRenderer

# TODO: need to add an "empty" template?


class DeletableFormRenderer(FormRenderer):
    """
    Renderer for the forms of a formset that can be deleted.

    The form will be rendered with two columns; a wider column for all the
    fields and a narrower (col-1) column for the delete button.
    """

    def get_form_container_class(self):
        """
        Return the CSS classes for the div that wraps the form fields and the
        delete button.
        """
        return "row mb-1 align-items-center py-1 form-container"

    def get_field_container_class(self):
        """Return the CSS classes for the div that wraps the form fields."""
        return "col fields-container"

    def get_delete_container_class(self):
        """Return the CSS classes for the div that wraps the delete button."""
        return "col-1 delete-container"

    def render(self):
        return format_html(
            '<div class="{container_class}">{form}</div>',
            container_class=self.get_form_container_class(),
            form=super().render(),
        )

    def render_fields(self):
        rendered_fields = rendered_delete = mark_safe("")
        kwargs = self.get_kwargs()
        renderer = get_field_renderer(**kwargs)
        for field in self.form:
            if field.name == DELETION_FIELD_NAME:
                # Render the widget without the label and without the wrapper:
                # TODO: implement a renderer for the deletion field, which adds
                #  the delete button (etc.). That way, FormsetDeletionWidget
                #  and the formset override in MIZInlineFormset could be omitted.
                rendered_delete = renderer(field, **kwargs).get_field_html()
            else:
                rendered_fields += renderer(field, **kwargs).render()
        return format_html(
            '<div class="{field_container_class}">{fields}</div><div class="{delete_wrapper_class}">{delete}</div>',
            field_container_class=self.get_field_container_class(),
            fields=rendered_fields,
            delete_wrapper_class=self.get_delete_container_class(),
            delete=rendered_delete,
        )


class DeletableFormsetRenderer(FormsetRenderer):

    def get_formset_container_class(self):
        """Return the CSS classes for the div that wraps the formset."""
        return f"{self.formset.prefix} formset-container"

    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            rendered_forms += DeletableFormRenderer(form, **kwargs).render()
        return format_html(
            '<div class="{formset_container}">{forms}</div>',
            formset_container=self.get_formset_container_class(),
            forms=rendered_forms,
        )
