from django.conf import settings
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required

schema_view_param = {
    'public': True,
    'permission_classes': (permissions.IsAdminUser,),
    'url': getattr(settings, 'SWAGGER_URL', None)
}

schema_view = get_schema_view(
    openapi.Info(
        title=settings.MICROSERVICE_TITLE + " API",
        default_version='v1',
        description='Microservice description'
    ),
    **schema_view_param,
)

urlpatterns = [
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
]
