from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.catalog"
    verbose_name = "Каталог"

    def ready(self):
        from .signals import watermark_img
        from .models import ProductImg, ProductCategoryGroup

        post_save.connect(
            watermark_img.watermark_img_signal,
            sender=ProductImg,
            weak=False,
            dispatch_uid="watermrk_img",
        )

        pre_save.connect(
            watermark_img.save_original_img, sender=ProductCategoryGroup, weak=False, dispatch_uid="save_original_img"
        )

        post_save.connect(
            watermark_img.watermark_img_category_signal,
            sender=ProductCategoryGroup,
            weak=False,
            dispatch_uid="watermrk_img_group",
        )
