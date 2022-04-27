from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .services import Google2FARequest, Google2FAHandler


class TwoFASerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code: str) -> str:
        request = self.context['request']
        secret: str = request.session.get('secret')
        if not secret:
            raise serializers.ValidationError(_('Probably QR code was not generated for activation'))
        service = Google2FARequest()
        valid: bool = service.validate_code(code, secret)
        if not valid:
            raise serializers.ValidationError(_('Entered code is not valid'))
        return code

    def validate(self, data: dict) -> dict:
        request = self.context['request']
        if request.user.enable_2fa:
            raise serializers.ValidationError(_("two factor authentication already enabled"))
        return data

    def save(self):
        request = self.context['request']
        secret: str = request.session.pop('secret')
        reserve_key: str = request.session.pop('reserve_key')
        user = Google2FAHandler.enable_user_2fa(request.user, secret, reserve_key)
        return user
