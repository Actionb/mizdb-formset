from django import template

from mizdb_inlines.renderers import DeletableFormsetRenderer

register = template.Library()


@register.simple_tag
def inline_formset(formset, **kwargs):
    return DeletableFormsetRenderer(formset, **kwargs).render()
