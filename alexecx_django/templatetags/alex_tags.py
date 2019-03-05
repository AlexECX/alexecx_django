from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=False)
def url_encode(base_dict=None, **kwargs):
    query = {}
    if base_dict is not None:
        if hasattr(base_dict, 'dict'):
            query.update(base_dict.dict())
        else:
            query.update(base_dict)
    query.update(kwargs)
    return urlencode(query)
