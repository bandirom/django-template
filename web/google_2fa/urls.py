from django.urls import path
from . import views

app_name = 'google_2fa'

urlpatterns = [
    path('qr-code/', views.Google2FAGenerateQRCodeView.as_view(), name='qr_code_generate'),
]


