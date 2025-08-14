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
    description = CKEditor5Field("описание", config_name="category", blank=True, null=True)

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
    image = models.ImageField("картинка", upload_to=category_group_image_upload_to, null=True)
    description = CKEditor5Field("описание", config_name="category", blank=True, null=True)

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
    categories = models.ManyToManyField(ProductCategory, related_name="products", verbose_name="категории товара")
    remainder = models.PositiveIntegerField("актуальный остаток", null=True, blank=True)
    stock = models.BooleanField("в наличии", default=True)
    best_price = models.BooleanField("гарантия лучшей цены", default=False)
    description = CKEditor5Field("описание товара", config_name="product")

    hidden = models.BooleanField("скрыть из каталога", default=False)

    @property
    def props(self):
        return 1

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    @property
    def first_image(self):
        image = self.images.first()
        if image:
            return image.url
        return None


class ProductPrice(AbstractOrderModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    name = models.CharField("вариация товара", max_length=24, blank=True)

    price = models.PositiveIntegerField("цена")
    discount = models.PositiveSmallIntegerField(
        "скидка (%)", blank=True, null=True, validators=[MaxValueValidator(99), MinValueValidator(1)]
    )

    class Meta(AbstractOrderModel.Meta):
        verbose_name = "цена"
        verbose_name_plural = "цены"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "product",
                    "name",
                ),
                name="unique_product_name",
            ),
            models.CheckConstraint(
                condition=models.Q(discount__gte=1) & models.Q(discount__lte=99),
                name="%(app_label)s_%(class)s_discount_range",
                violation_error_message="Скидка должна быть в диапазоне от 1 до 99",
            ),
        ]

    def __str__(self):
        return self.name if self.name else str(self.price) + " Руб"


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


# redirects
class AbstractRedirectsFrom(models.Model):
    old_slug = models.CharField("старый url", max_length=60, unique=True)

    def __str__(self):
        return f"старый слаг: {self.old_slug}; к: {self.to.name}"

    class Meta:
        abstract = True
        verbose_name = "Старый слаг (url)"
        verbose_name_plural = "Старые слаги (url)"


class ProductRedirectFrom(AbstractRedirectsFrom):
    to = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductCategoryGroupRedirectFrom(AbstractRedirectsFrom):
    to = models.ForeignKey(ProductCategoryGroup, on_delete=models.CASCADE)


class ProductCategoryRedirectFrom(AbstractRedirectsFrom):
    to = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
