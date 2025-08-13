from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from shared.utils import commercial_request_file_upload_to
from apps.catalog.models import Product, ProductPrice
from .validators import FileValidator


# Create your models here.
class AbstractBaseRequest(models.Model):
    name = models.CharField("имя", max_length=32, validators=[MinLengthValidator(2), MaxLengthValidator(32)])
    phone = models.CharField("номер телефона", max_length=20)
    comment = models.TextField("комментарий", blank=True)
    addition = models.TextField("доп. информация", blank=True)
    date = models.DateTimeField("дата", auto_now_add=True)

    class Meta:
        abstract = True


class CommercialRequest(AbstractBaseRequest):
    file = models.FileField(
        "чертеж",
        upload_to=commercial_request_file_upload_to,
        validators=[FileValidator(content_types=("application/pdf"), max_size=10485760)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "запрос коммерческого предложения"
        verbose_name_plural = "запросы коммерческих предложений"

    def __str__(self):
        return f"Запрос коммерческого предложения {self.name} - {self.phone}"


class ConsultationRequest(AbstractBaseRequest):

    class Meta:
        verbose_name = "запрос консультации"
        verbose_name_plural = "запросы консультаций"

    def __str__(self):
        return f"Запрос консультации {self.name} - {self.phone}"


class OrderRequest(AbstractBaseRequest):

    class Meta:
        verbose_name = "запрос товаров"
        verbose_name_plural = "запросы товаров"

    def __str__(self):
        return f"Запрос товаров {self.name} - {self.phone}"


class OrderRequestItem(models.Model):
    order = models.ForeignKey(OrderRequest, models.CASCADE, related_name="items", verbose_name="заказ")
    product = models.ForeignKey(Product, models.SET_NULL, null=True, verbose_name="товар")
    quantity = models.PositiveIntegerField("количество")
    price = models.PositiveIntegerField("цена на момент запроса со скидкой")

    variant = models.ForeignKey(
        ProductPrice, models.SET_NULL, null=True, verbose_name="текущее название вариации товара"
    )
    variant_text = models.CharField("название вариации на момент запроса", max_length=24)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return "Товар"
