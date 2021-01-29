from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required


schema_view = get_schema_view(
    openapi.Info(
        title="Service API",
        default_version='v1',

    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]
