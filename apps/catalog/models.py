from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from shared.utils import category_group_image_upload_to, product_image_upload_to, product_file_upload_to


# Create your models here.
class AbstractOrderModel(models.Model):
    order = models.PositiveSmallIntegerField("очередность", default=32000)

    class Meta:
        abstract = True
        ordering = (
            "order",
            "id",
        )


class ProductCategoryGroup(AbstractOrderModel):
    name = models.CharField("название", max_length=48, unique=True)
    slug = models.SlugField("url (slug)", max_length=64, unique=True)
    image = models.ImageField("картинка", upload_to=category_group_image_upload_to, null=True)

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "группа категории товара"
        verbose_name_plural = "группы категории товаров"

    def __str__(self):
        return self.name


class ProductCategory(AbstractOrderModel):
    name = models.CharField("название", max_length=48, unique=True)
    slug = models.SlugField("url (slug)", max_length=64, unique=True)
    group = models.ForeignKey(
        ProductCategoryGroup, related_name="categories", on_delete=models.RESTRICT, verbose_name="группа категории"
    )

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "категория товара"
        verbose_name_plural = "категории товаров"

    def __str__(self):
        return self.name


class Attribute(AbstractOrderModel):
    name = models.CharField("название", max_length=24)

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="attributes")

    class Meta:
        verbose_name = "характеристика категории товаров"
        verbose_name_plural = "характеристики категорий товаров"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "name",
                    "category",
                ),
                name="unique_attribute_name_category",
            ),
        ]

    def __str__(self):
        return self.name


class Product(AbstractOrderModel):
    name = models.CharField("название", max_length=80, unique=True)
    slug = models.SlugField("url (slug)", max_length=96, unique=True)
    category = models.ForeignKey(
        ProductCategory, models.PROTECT, related_name="products", verbose_name="категория товара"
    )
    price = models.PositiveIntegerField("цена")
    discount = models.PositiveSmallIntegerField(
        "скидка (%)", blank=True, null=True, validators=[MaxValueValidator(99), MinValueValidator(1)]
    )
    remainder = models.PositiveIntegerField("актуальный остаток")
    stock = models.BooleanField("в наличии", default=True)
    # code = models.CharField("артикул", max_length=32, unique=True, db_index=True)
    description = CKEditor5Field("описание товара", config_name="product")

    @property
    def props(self):
        return 1

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "товар"
        verbose_name_plural = "товары"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(discount__gte=1) & models.Q(discount__lte=99),
                name="%(app_label)s_%(class)s_discount_range",
                violation_error_message="Скидка должна быть в диапазоне от 1 до 99",
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def first_image(self):
        return self.images.first()


class AttributeValue(models.Model):
    name = models.CharField("название", max_length=24)

    attribute = models.ForeignKey(
        Attribute,
        models.CASCADE,
        related_name="values",
        verbose_name="значение характеристики товара",
    )

    class Meta:
        verbose_name = "значение характеристики товаров"
        verbose_name_plural = "значения характеристик товаров"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "name",
                    "attribute",
                ),
                name="unique_attribute_value_name_attribute",
            ),
        ]

    def __str__(self):
        return self.name


class ProductImg(models.Model):
    url = models.ImageField("изображение товара", upload_to=product_image_upload_to)
    product = models.ForeignKey(Product, models.CASCADE, related_name="images", verbose_name="товар")

    order = models.PositiveSmallIntegerField("очередность", default=10)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товара"
        ordering = ("product", "order", "id")


class ProductDoc(models.Model):
    name = models.CharField("название документа", max_length=100)
    url = models.FileField("документ", upload_to=product_file_upload_to)
    product = models.ForeignKey(Product, models.CASCADE, related_name="docs", verbose_name="товар")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "документ товара"
        verbose_name_plural = "документы товаров"


class ProductAttribute(AbstractOrderModel):
    product = models.ForeignKey(Product, models.CASCADE, related_name="attributes", verbose_name="товар")
    attribute = models.ForeignKey(
        Attribute, models.CASCADE, related_name="attribute_products", verbose_name="характеристика"
    )
    value = models.ForeignKey(AttributeValue, models.CASCADE, verbose_name="значение")

    def __str__(self):
        return self.product.name + " " + self.attribute.name + " " + self.value.name

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "характеристика товара"
        verbose_name_plural = "характеристики товаров"
        constraints = [
            models.UniqueConstraint(
                fields=("product", "attribute"),
                name="unique_product_attribute",
            ),
        ]
