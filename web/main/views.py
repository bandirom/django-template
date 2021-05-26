from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser

from .serializers import UserSerializer, SetTimeZoneSerializer


User = get_user_model()


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request):
        """Current user view

            Using this construction you can load related fields (select_related and prefetch_related) in queryset
        """

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class SetUserTimeZone(GenericAPIView):
    serializer_class = SetTimeZoneSerializer
    parser_classes = (FormParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response()
        response.set_cookie(
            key=getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone'),
            value=serializer.data.get('timezone'),
            max_age=getattr(settings, 'TIMEZONE_COOKIE_AGE', 86400),
        )
        return response
