from django.urls import path
from . import views

app_name = 'google_2fa'

urlpatterns = [
    path('login/confirm/', views.Login2FAView.as_view(), name='login_2fa_confirm'),
    path('qr-code/', views.TwoFAGenerateQRCodeView.as_view(), name='qr_code_generate'),
    path('qr-code/confirm/', views.Activate2FAView.as_view(), name='qr_code_confirm'),
]


