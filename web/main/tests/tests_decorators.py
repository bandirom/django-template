from time import sleep

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from main import decorators

User = get_user_model()

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

locmem_cache = override_settings(CACHES=CACHES)


class DecoratorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test111@test.com', password='test_test_test')

    @decorators.except_shell((User.DoesNotExist,))
    def get_user(self, email):
        return User.objects.get(email=email)

    def test_except_decorator(self):
        test_user = self.get_user(email='test111@test.com')
        self.assertEqual(test_user, self.user)
        self.assertEqual(test_user.email, self.user.email)
        non_exist = self.get_user(email='non_exist_user@test.com')
        self.assertEqual(non_exist, None)
