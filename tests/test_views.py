from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import modify_settings
from django.utils import timezone
from rest_framework.reverse import reverse_lazy
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

User = get_user_model()


class ViewsTest(APITestCase):
    @modify_settings(
        MIDDLEWARE={
            'append': 'main.middleware.TimezoneMiddleware',
        }
    )
    def test_set_timezone(self):
        test_timezone = 'Europe/Kyiv'
        user = User.objects.get(email=settings.SUPERUSER_EMAIL)

        self.client.force_login(user)

        url = reverse_lazy('set_user_timezone')
        data = {'timezone': test_timezone}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, response.data)
        self.assertEqual(response.data['timezone'], test_timezone)
        self.assertEqual(
            response.cookies.get(getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')).value, test_timezone
        )
        # Request need to activate timezone after set cookies
        self.client.get('/')
        self.assertEqual(timezone.get_current_timezone_name(), test_timezone)
