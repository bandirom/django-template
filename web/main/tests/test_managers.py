from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='tom.cruize@test.com', password='password1234', first_name='Tom', last_name='Cruise'
        )
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'tom.cruize@test.com')
        self.assertEqual(user.full_name, 'Tom Cruise')

    def test_create_super_user(self):
        user = User.objects.create_superuser(email='super_tester@test.com', password='password1234')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
