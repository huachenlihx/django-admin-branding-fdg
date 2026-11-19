from django import template

from .. import conf

register = template.Library()


@register.simple_tag
def branding(name):
    """Raw option value, or empty string when unset."""
    return conf.get(name) or ""


@register.simple_tag
def branding_url(name):
    """Option resolved to a URL (static path -> static URL), or empty string."""
    return conf.resolve_url(conf.get(name))
