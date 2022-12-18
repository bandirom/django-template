from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import RedirectView

from .views import SetUserTimeZone

urlpatterns = [
    path('', login_required(RedirectView.as_view(pattern_name='admin:index'))),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
    path('login/', LoginView.as_view(template_name='rest_framework/login.html'), name='rest_login'),
]
