
from django import template

register = template.Library()


@register.inclusion_tag('django_ogp/ogp_meta.html', takes_context=True, name='add_ogp_meta')
def do_add_ogp_meta(context):
    """
    """
    view = context.get('view', {})
    ogp = view.ogp if hasattr(view, 'ogp') else None
    ogp_custom = view.ogp_custom if hasattr(view, 'ogp_custom') else None
    return {'ogp': ogp, 'ogp_custom': ogp_custom}
