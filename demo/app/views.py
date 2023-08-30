from django.forms import inlineformset_factory
from django.views.generic import UpdateView

from .models import Contact, PhoneNumber


class ContactView(UpdateView):
    model = Contact
    fields = "__all__"
    template_name = "contact.html"
    success_url = "/"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.kwargs[self.pk_url_kwarg] = 1

    def get_formset_class(self):
        return inlineformset_factory(Contact, PhoneNumber, fields=["label", "number"], extra=1)

    def get_formset(self, **kwargs):
        return self.get_formset_class()(instance=self.object, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"] = self.get_formset()
        ctx["header"] = "Contact Form"
        return ctx

    def form_valid(self, form):
        formset = self.get_formset(data=self.request.POST)
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)
