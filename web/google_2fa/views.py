import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .permissions import UserNotActive2FA
from .services import Google2FAHandler
from . import serializers

logger = logging.getLogger(__name__)


class TwoFAGenerateQRCodeView(APIView):
    permission_classes = (UserNotActive2FA, )

    def get(self, request):
        handler = Google2FAHandler()
        data = handler.generate_user_qr_code(request.user)
        request.session['reserve_key'] = data['reserve_key']
        request.session['secret'] = data['secret']
        return Response(data, status=status.HTTP_200_OK)


class Activate2FAView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TwoFASerializer
