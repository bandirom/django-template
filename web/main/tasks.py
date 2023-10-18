from os import path
from smtplib import SMTPRecipientsRefused
from typing import Any, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags
from django.utils.translation import activate

from src.celery import app


class SendingEmailTaskArgs(app.Task):
    autoretry_for = (SMTPRecipientsRefused, ConnectionRefusedError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 5
    retry_jitter = True


@app.task(name='email.send_information_email', base=SendingEmailTaskArgs)
def send_information_email(
    *,
    subject: str,
    template_name: str,
    context: dict,
    to_email: list[str] | str,
    letter_language: str = 'en',
    **kwargs: Optional[Any],
) -> bool:
    """
    :param subject: email subject
    :param template_name: template path to email template
    :param context: data what will be passed into email
    :param to_email: receiver email(s)
    :param letter_language: translate letter to selected lang
    :param kwargs: from_email, bcc, cc, reply_to and file_path params
    """
    activate(letter_language)
    _to_email: list[str] = [to_email] if isinstance(to_email, str) else to_email
    html_email: str = loader.render_to_string(template_name, context)

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html_email),
        to=_to_email,
        from_email=kwargs.get('from_email'),
        bcc=kwargs.get('bcc'),
        cc=kwargs.get('cc'),
        reply_to=kwargs.get('reply_to'),
    )
    if file_path := kwargs.get('file_path'):
        file_path = path.join(settings.BASE_DIR, file_path)
        email_message.attach_file(file_path, kwargs.get('mimetype'))
    email_message.send()
    return True
