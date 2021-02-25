from django.conf import settings
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required

schema_view_param = {
    'public': True,
    'permission_classes': (permissions.IsAdminUser,),
}

if settings.USE_HTTPS:
    schema_view_param['url'] = getattr(settings, 'CURRENT_HOST', 'http://localhost')

schema_view = get_schema_view(
    openapi.Info(
        title="Service API",
        default_version='v1',
        description='Microservice for Customer StemSC'
    ),
    **schema_view_param,
)

urlpatterns = [
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
]
