from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
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
        return f"{self.formset.prefix} formset-container mb-3"

    def get_add_button_class(self):
        """Return the CSS classes for the add button."""
        return "btn btn-outline-success add-btn"

    def get_add_button_label(self):
        """Return the label for the add button."""
        img = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>"""
        label = gettext("Add another %(verbose_name)s") % {"verbose_name": self.formset.model._meta.verbose_name}
        return img + f'<span class="align-middle">{label}</span'

    def get_add_button_html(self):
        """Return the HTML for the button that adds another form to the formset."""
        return mark_safe(f'<button class="{self.get_add_button_class()}">{self.get_add_button_label()}</button>')

    def get_add_row_html(self):
        """
        Return the HTML for the div with the add button and the empty form
        template.
        """
        empty_form = DeletableFormRenderer(self.formset.empty_form, **self.get_kwargs()).render()
        return mark_safe(
            '<div class="add-row">'
            f'<div class="empty-form d-none">{empty_form}</div>'
            f"{self.get_add_button_html()}</div>"
        )

    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            rendered_forms += DeletableFormRenderer(form, **kwargs).render()
        return rendered_forms

    def render(self):
        return format_html(
            '<div class="{formset_container}">{html}{add_row}</div>',
            formset_container=self.get_formset_container_class(),
            html=super().render(),
            add_row=self.get_add_row_html(),
        )
