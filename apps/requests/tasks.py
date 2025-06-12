from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger

from core.celery import app


logger = get_task_logger("stroy.email")


@app.task(bind=True)
def run_send_email(self, subject, message, sender, receiver):
    logger.info(f"Sending email in celery;")
    try:
        logger.info(f"Sending email celery;")
        send_mail(subject, message, sender, receiver, fail_silently=False)
    except SMTPException as e:
        logger.info(f"Sending email celery failed; {e}")
        raise self.retry(exc=e, countdown=2 * 60)
