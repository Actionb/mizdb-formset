from django.forms import inlineformset_factory
from django.views.generic import UpdateView

from mizdb_inlines.views import InlineFormsetMixin

from .models import Contact, PhoneNumber


class ContactView(InlineFormsetMixin, UpdateView):
    model = Contact
    fields = "__all__"
    template_name = "contact.html"
    success_url = "/"

    formset_classes = (inlineformset_factory(Contact, PhoneNumber, fields=["label", "number"], extra=1),)

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.kwargs[self.pk_url_kwarg] = 1
