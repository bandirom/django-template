from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .yasg import urlpatterns as swagger_url

admin_url = settings.ADMIN_URL

urlpatterns = [
    path('', include('main.urls')),
    path(f'{admin_url}/', admin.site.urls),
    path(f'{admin_url}/defender/', include('defender.urls')),
    path('api/', include('rest_framework.urls')),
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += swagger_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.ENABLE_SILK:
        urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
