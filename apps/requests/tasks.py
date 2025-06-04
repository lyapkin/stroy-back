import logging
from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings

from core.celery import app


logger = logging.getLogger("stroy.email")


@app.task(bind=True)
def run_send_email(self, subject, message):
    try:
        if settings.EMAIL_HOST_USER:
            logger.info(f"Sending email celery;")
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    except SMTPException as e:
        logger.info(f"Sending email celery failed; {e}")
        raise self.retry(exc=e, countdown=2 * 60)
