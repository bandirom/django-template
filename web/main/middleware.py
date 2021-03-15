from django.utils.deprecation import MiddlewareMixin


class RemoteUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user_id = None
        if user_id := request.headers.get('Remote-User'):
            request.user_id = int(user_id)
        elif request.user.is_authenticated:
            request.user_id = request.user.id
