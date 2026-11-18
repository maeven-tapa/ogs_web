"""Icons from the Lucide sprite included in the initial page HTML."""
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def icon(name, css_class=""):
    return format_html(
        '<svg class="icon {}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<use href="#icon-{}"></use></svg>',
        css_class,
        name,
    )
