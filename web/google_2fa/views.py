import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .permissions import UserWithNotActive2FA
from .services import Google2FAHandler

logger = logging.getLogger(__name__)


class TwoFAGenerateQRCodeView(APIView):
    permission_classes = (UserWithNotActive2FA,)

    def get(self, request):
        handler = Google2FAHandler()
        data = handler.generate_user_qr_code(request.user)
        request.session['reserve_key'] = data['reserve_key']
        request.session['secret'] = data['secret']
        return Response(data, status=status.HTTP_200_OK)


class Activate2FAView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.Activate2FASerializer


class Login2FAView(GenericAPIView):
    serializer_class = serializers.Login2FASecondStepSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
