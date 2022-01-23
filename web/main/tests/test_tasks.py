from django.core import mail
from django.test import TestCase, override_settings

from main import tasks

locmem_email_backend = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)


class CeleryTaskTestCase(TestCase):
    @locmem_email_backend
    def test_send_information_email(self):
        data = {
            'subject': 'Test',
            'context': {
                'test123': '456',
            },
            'template_name': 'user_timezone.html',
            'to_email': 'test@test.com',
        }
        tasks.send_information_email.delay(**data)
        self.assertEqual(len(mail.outbox), 1)
