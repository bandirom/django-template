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

    @decorators.execution_time(stdout='console')
    def time_measure_console(self):
        return 'Hello World'

    @decorators.execution_time(stdout='tuple')
    def time_measure_tuple(self):
        sleep(1)
        return 'Hello World'

    @decorators.execution_time(stdout='tuple')
    @decorators.cached_function_result(timeout=5)
    def cached_result_function(self, sleep_time: int = 2):
        sleep(sleep_time)
        return 'Result after hard func'

    def test_except_decorator(self):
        test_user = self.get_user(email='test111@test.com')
        self.assertEqual(test_user, self.user)
        self.assertEqual(test_user.email, self.user.email)
        non_exist = self.get_user(email='non_exist_user@test.com')
        self.assertEqual(non_exist, None)

    def test_execution_time(self):
        data = self.time_measure_console()
        self.assertEqual(data, 'Hello World')

        data, delta = self.time_measure_tuple()
        self.assertEqual(data, 'Hello World')
        self.assertGreater(delta, 1, f'Delta: {delta}')

    @locmem_cache
    def test_cached_function_result(self):
        sleep_time = 2
        data, delta = self.cached_result_function(sleep_time)
        self.assertEqual(data, 'Result after hard func')
        self.assertGreater(delta, sleep_time, f'Delta: {delta}')
        data, delta = self.cached_result_function(sleep_time)
        self.assertLess(delta, 0.1, f'Delta: {delta}')
