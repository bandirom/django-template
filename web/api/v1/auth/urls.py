from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('sign-in/', views.LoginView.as_view(), name='sign-in'),
]
