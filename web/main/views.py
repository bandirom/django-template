from typing import TYPE_CHECKING

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SetTimeZoneSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ''

    @extend_schema(exclude=True)
    def get(self, request: 'Request', *args, **kwargs):
        return Response()


class SetUserTimeZone(GenericAPIView):
    serializer_class = SetTimeZoneSerializer
    authentication_classes = (SessionAuthentication,)

    def post(self, request: 'Request'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data)
        response.set_cookie(
            key=getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone'),
            value=serializer.data.get('timezone'),
            max_age=getattr(settings, 'TIMEZONE_COOKIE_AGE', 86400),
        )
        return response
