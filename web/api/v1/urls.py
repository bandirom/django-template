from django.urls import include, path  # noqa: F401

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
]
