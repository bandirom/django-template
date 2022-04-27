from django.contrib import admin
from .models import Google2FA


@admin.register(Google2FA)
class Google2FAAdmin(admin.ModelAdmin):
    pass

