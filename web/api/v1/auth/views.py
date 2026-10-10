from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from . import serializers
from .services import LoginService


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        service = LoginService(request)
        user = service.validate_user_credentials(**serializer.validated_data)
        return service.get_response(user)
