from django.contrib.auth import get_user_model
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    password = PostGenerationMethodCall('set_password', 'secret')

    class Meta:
        model = User
        django_get_or_create = ('email',)
