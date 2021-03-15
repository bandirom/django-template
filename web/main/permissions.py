from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class HasApiKeyOrIsAuthenticated(IsAuthenticated):

    def has_permission(self, request, view):
        if key := request.headers.get('Authorization'):
            token = list(key.split(" "))
            if token[0] == settings.API_KEY_HEADER and token[1] == settings.API_KEY:
                return True
        print("HELLO from Template")
        return super(HasApiKeyOrIsAuthenticated, self).has_permission(request, view)
