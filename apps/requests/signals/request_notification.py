import logging
from django.dispatch import Signal
from django.conf import settings

from ..tasks import run_send_email


order_ready = Signal()
logger = logging.getLogger("stroy.email")


def email_notification_on_call_request(sender, instance=None, created=False, **kwargs):
    if created and settings.EMAIL_HOST_USER:
        logger.info(f"Sending email starts; {settings.EMAIL_HOST_USER}")
        subject = "Запрос консультации с сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос консультации с сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
        )

        run_send_email.delay(subject, message)


def email_notification_on_order_request(sender, instance=None, created=False, **kwargs):
    if created and settings.EMAIL_HOST_USER:
        logger.info(f"Sending email starts; {settings.EMAIL_HOST_USER}")
        subject = "Запрос из корзины сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос из корзины сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
        )

        run_send_email.delay(subject, message)


def email_notification_on_commercial_request(sender, instance=None, created=False, **kwargs):
    if created and settings.EMAIL_HOST_USER:
        logger.info(f"Sending email starts; {settings.EMAIL_HOST_USER}")
        subject = "Запрос коммерческого предложения сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос коммерческого предложения сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
        )

        run_send_email.delay(subject, message)
