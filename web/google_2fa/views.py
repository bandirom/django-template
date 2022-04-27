import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import Google2FARequest
from . import serializers

logger = logging.getLogger(__name__)


class Google2FAGenerateQRCodeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        service = Google2FARequest()
        url = service.qr_code_generate(request.user.email)
        return Response({'url': url}, status=status.HTTP_200_OK)
