from django import template

from mizdb_inlines.renderers import MIZFormsetRenderer

register = template.Library()


@register.simple_tag
def inline_formset(formset, **kwargs):
    return MIZFormsetRenderer(formset, **kwargs).render()
