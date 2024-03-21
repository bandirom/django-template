from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('', login_required(RedirectView.as_view(pattern_name='admin:index'))),
]
