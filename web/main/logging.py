import platform
import time
from django.conf import settings
from django.utils.log import AdminEmailHandler as _AdminEmailHandler

from pythonjsonlogger.jsonlogger import JsonFormatter as BaseFormatter

from main.tasks import send_information_email


class JsonFormatter(BaseFormatter):
    converter = time.gmtime

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["hostname"] = platform.node()


class AdminEmailHandler(_AdminEmailHandler):

    def send_mail(self, subject, message, *args, **kwargs):
        if not settings.ADMINS:
            return
        if not all(isinstance(a, (list, tuple)) and len(a) == 2 for a in settings.ADMINS):
            raise ValueError('The ADMINS setting must be a list of 2-tuples.')
        data: dict = {
            'subject': subject,
            'template_name': 'emails/admin_error_handler.html',
            'context': {
                'html_message': kwargs.get('html_message'),
            },
            'from_email': settings.SERVER_EMAIL,
            'to_email': [a[1] for a in settings.ADMINS]
        }
        send_information_email.delay(**data)
