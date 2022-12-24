from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

schema_view_param = {
    'public': True,
    'permission_classes': (permissions.IsAdminUser,),
    'url': getattr(settings, 'SWAGGER_URL', None),
    'authentication_classes': (SessionAuthentication,),
}

schema_view = get_schema_view(
    openapi.Info(
        title=f'{settings.PROJECT_TITLE} API',
        default_version='v1',
        description='Project description',
    ),
    **schema_view_param,
)

urlpatterns = [
    path(
        'swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'
    ),
]
