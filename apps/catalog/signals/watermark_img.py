from django.dispatch import Signal
from ..tasks import watermark_img_task


order_ready = Signal()


def watermark_img_signal(sender, instance=None, created=False, **kwargs):
    if instance:
        watermark_img_task.delay(instance.url.path)


def save_original_img(sender, instance=None, **kwargs):
    if instance:
        instance.__original_img_name = instance.image.name


def watermark_img_category_signal(sender, instance=None, created=False, **kwargs):
    if instance and instance.__original_img_name != instance.image.name:
        watermark_img_task.delay(instance.image.path)
