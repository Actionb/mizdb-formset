from django.forms import BaseInlineFormSet

from mizdb_inlines.widgets import FormsetDeletionWidget


class MIZInlineFormset(BaseInlineFormSet):
    deletion_widget = FormsetDeletionWidget
