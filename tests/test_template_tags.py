from django.conf import settings
from django.test import TestCase

from main.templatetags import main


class TestTemplateTags(TestCase):
    def test_microservice_title(self):
        self.assertEqual(main.microservice_title(), settings.MICROSERVICE_TITLE)

    def test_timezone_cookie_name(self):
        self.assertEqual(main.timezone_cookie_name(), 'timezone')
