from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def project_title() -> str:
    return settings.PROJECT_TITLE


@register.simple_tag
def timezone_cookie_name() -> str:
    return getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')
