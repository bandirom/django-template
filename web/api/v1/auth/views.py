from typing import TYPE_CHECKING

from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from . import serializers
from .services import LoginService

if TYPE_CHECKING:
    from rest_framework.request import Request


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    response_serializer_class = serializers.LoginResponseSerializer
    permission_classes = (AllowAny,)

    def post(self, request: "Request") -> "Response":
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = LoginService(request, settings=settings.REST_AUTH)
        user = service.validate_user_credentials(**serializer.validated_data)
        tokens = service.get_tokens(user)
        response_serializer = self.response_serializer_class(tokens)

        response = Response(response_serializer.data, status=HTTP_200_OK)
        service.set_cookies(response, tokens)
        return response
