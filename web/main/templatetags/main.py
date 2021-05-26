from django import template
from django.conf import settings

register = template.Library()

title = settings.MICROSERVICE_TITLE


@register.simple_tag
def microservice_title():
    return title


@register.simple_tag
def timezone_cookie_name():
    return getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')
