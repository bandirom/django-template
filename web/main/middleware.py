import pytz
from django.http import HttpResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META["PATH_INFO"] == settings.HEALTH_CHECK_URL:
            return HttpResponse("pong")


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if tzname := request.COOKIES.get(getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')):
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
