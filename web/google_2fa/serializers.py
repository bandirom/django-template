from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .services import Google2FARequest, Google2FAHandler
from . import app_settings


class ValidateCodeMixin(serializers.Serializer):
    code = serializers.CharField()


class Activate2FASerializer(ValidateCodeMixin, serializers.Serializer):

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
            raise serializers.ValidationError(_("Two factor authentication already enabled"))
        return data

    def save(self):
        request = self.context['request']
        secret: str = request.session.pop('secret')
        reserve_key: str = request.session.pop('reserve_key')
        user = Google2FAHandler.enable_user_2fa(request.user, secret, reserve_key)
        return user


class Login2FASecondStepSerializer(ValidateCodeMixin):

    def validate(self, data: dict):
        code: str = data['code']
        request = self.context['request']
        handler = Google2FAHandler()
        user_id = int(request.session.pop('user_id', 1))
        user = handler.get_user(user_id)
        if len(code) > app_settings.TWO_FA_CODE_LENGTH:
            valid: bool = handler.validate_reserve_key(code, user.two_fa.reserve_key,)
            if not valid:
                raise serializers.ValidationError(_("Reserve key is not valid"))
            handler.deactivate_user_2fa(user)
            return {"status": "deactivated_2fa"}
        service = Google2FARequest()
        valid: bool = service.validate_code(code, user.two_fa.secret)
        if not valid:
            raise serializers.ValidationError(_('Entered code is not valid'))
        return
