from os import environ
from typing import Union

from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate

from main.decorators import smtp_shell
from src.celery import app


@app.task(name='email.send_information_email')
def send_information_email(
    subject: str,
    template_name: str,
    context: dict,
    to_email: Union[list[str], str],
    letter_language: str = 'en',
    **kwargs,
):
    """
    :param subject: email subject
    :param template_name: template path to email template
    :param context: data what will be passed into email
    :param to_email: receiver email(s)
    :param letter_language: translate letter to selected lang
    :param kwargs: from_email, bcc, cc, reply_to and file_path params
    """
    activate(letter_language)
    to_email: list = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(
        subject=subject,
        from_email=kwargs.get('from_email'),
        to=to_email,
        bcc=kwargs.get('bcc'),
        cc=kwargs.get('cc'),
        reply_to=kwargs.get('reply_to'),
    )
    html_email: str = loader.render_to_string(template_name, context)
    email_message.attach_alternative(html_email, 'text/html')
    if file_path := kwargs.get('file_path'):
        file_path = environ.get('APP_HOME', environ.get('HOME')) + file_path
        email_message.attach_file(file_path, kwargs.get('mimetype'))
    return send_email(email_message)


@smtp_shell
def send_email(email_message: EmailMultiAlternatives):
    email_message.send()
    return True
