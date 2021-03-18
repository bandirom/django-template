from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class RemoteUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user_id = None
        if user_id := request.headers.get('Remote-User'):
            request.user_id = int(user_id)
        elif request.user.is_authenticated:
            request.user_id = request.user.id


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META["PATH_INFO"] == settings.LB_HEALTH_CHECK_URL:
            return HttpResponse("pong")
