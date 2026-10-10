from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from main.models import UserT

User = get_user_model()


class UserQueryService:
    queryset: QuerySet[User] = User.objects.all()

    def get_by_email(self, email: str) -> UserT | None:
        return self.queryset.filter(email=email).first()
