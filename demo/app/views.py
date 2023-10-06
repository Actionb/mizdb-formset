from django import forms
from django.views.generic import UpdateView

from mizdb_inlines.views import InlineFormsetMixin

from .models import Contact, PhoneNumber


class ContactView(InlineFormsetMixin, UpdateView):
    model = Contact
    fields = "__all__"
    template_name = "contact.html"
    success_url = "/"

    formset_classes = (
        forms.inlineformset_factory(
            Contact,
            PhoneNumber,
            fields=["label", "number"],
            widgets={"label": forms.Select(choices=[("", "-----"), ("Home", "Home"), ("Work", "Work")])},
            extra=1,
        ),
    )

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.kwargs[self.pk_url_kwarg] = 1
