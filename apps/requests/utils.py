import logging
from django.conf import settings
from .tasks import run_send_email

logger = logging.getLogger("stroy.email")


def send_email_notification(subject, message):
    if settings.EMAIL_HOST_USER and settings.EMAIL_FORM_NOTIFICATION_RECEIVER:
        logger.info(f"Sending email starts; {settings.EMAIL_HOST_USER}")
        run_send_email.delay(subject, message, settings.EMAIL_HOST_USER, settings.EMAIL_FORM_NOTIFICATION_RECEIVER)
