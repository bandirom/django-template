from typing import TYPE_CHECKING, Optional

import pytz
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

if TYPE_CHECKING:
    from django.http import HttpRequest


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request: 'HttpRequest') -> Optional[HttpResponse]:
        if request.META['PATH_INFO'] == settings.HEALTH_CHECK_URL:
            return HttpResponse('pong')


class TimezoneMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: 'HttpRequest'):
        if tzname := request.COOKIES.get(getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')):
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
