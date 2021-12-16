from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK


class MiddlewareTest(APITestCase):
    def test_health_check_middleware(self):
        url = settings.HEALTH_CHECK_URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(type(response.content), bytes)
        self.assertEqual(response.content.decode('utf-8'), 'pong')
