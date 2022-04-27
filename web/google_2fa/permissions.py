from rest_framework.permissions import BasePermission


class UserWithNotActive2FA(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and not request.user.enable_2fa
