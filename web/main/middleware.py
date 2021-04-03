from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META["PATH_INFO"] == settings.HEALTH_CHECK_URL:
            return HttpResponse("pong")
