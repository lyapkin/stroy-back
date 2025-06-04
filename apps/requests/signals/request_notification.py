from django.dispatch import Signal
from django.conf import settings

from ..tasks import run_send_email


order_ready = Signal()


def email_notification_on_request(sender, instance=None, created=False, **kwargs):
    if created and settings.EMAIL_HOST_USER:
        subject = "Запрос звонка: " + instance.name + " - " + instance.phone
        message = f"Запрос звонка.\n\n" f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"

        run_send_email.delay(subject, message)
