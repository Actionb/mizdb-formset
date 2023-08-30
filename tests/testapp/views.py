from django.forms import inlineformset_factory
from django.views.generic import UpdateView

from tests.testapp.models import Contact, PhoneNumber

FORMSET_PREFIX = "foo_bar"


class ContactView(UpdateView):
    model = Contact
    fields = "__all__"
    template_name = "contact.html"

    def get_success_url(self):
        return self.request.path

    def get_formset_class(self):
        return inlineformset_factory(Contact, PhoneNumber, fields=["label", "number"], extra=2)

    def get_formset(self, **kwargs):
        return self.get_formset_class()(instance=self.object, prefix=FORMSET_PREFIX, **kwargs)

    def get_context_data(self, formset=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"] = formset or self.get_formset()
        ctx["header"] = "Contact Form"
        return ctx

    def form_valid(self, form):
        formset = self.get_formset(data=self.request.POST)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        formset = self.get_formset(data=self.request.POST)
        formset.full_clean()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
