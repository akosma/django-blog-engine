from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def get_static_url():
    return str( settings.STATIC_URL )
