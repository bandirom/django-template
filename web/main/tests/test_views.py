from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK


User = get_user_model()


class ViewsTest(APITestCase):

    def test_set_timezone(self):
        user = User.objects.get(email=settings.SUPERUSER_EMAIL)

        self.client.force_login(user)

        url = reverse_lazy('set_user_timezone')
        data = {
            'timezone': 'Europe/Kiev'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, response.data)
        self.assertEqual(response.data['timezone'], 'Europe/Kiev')

