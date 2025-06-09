from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.pages.models import Page
from apps.blog.models import Post
from apps.catalog.models import Product, ProductCategoryGroup, ProductCategory
from apps.catalog.catalog_types import PRODUCT, CATEGORY_GROUP, CATEGORY
from .mixins import MetaGenerationRuleMixin


# Create your models here.
class Robots(models.Model):
    text = models.TextField("robots.txt")

    class Meta:
        verbose_name = "robots.txt"
        verbose_name_plural = "robots.txt"

    def __str__(self) -> str:
        return "robots.txt"


class Sitemap(models.Model):
    pass


# metadata
class MetaGenerationRule(models.Model):
    default_types = {
        CATEGORY_GROUP: "grp",
        CATEGORY: "ctg",
        PRODUCT: "prd",
    }

    choices = {
        default_types[CATEGORY_GROUP]: "Группа категорий",
        default_types[CATEGORY]: "Категория",
        default_types[PRODUCT]: "Товар",
    }

    type = models.CharField("тип", max_length=3, choices=choices, primary_key=True)
    title = models.CharField("правило генерации Title", max_length=255)
    description = models.TextField("правило генерации Description")

    def __str__(self):
        return self.choices[self.type]

    class Meta:
        verbose_name = "правило генерации метатегов"
        verbose_name_plural = "правила генерации метатегов"


class AbstractPageMetadata(models.Model):
    CHANGE_FREQ_CHOICES = {
        "always": "always",
        "hourly": "hourly",
        "daily": "daily",
        "weekly": "weekly",
        "monthly": "monthly",
        "yearly": "yearly",
        "never": "never",
    }

    title = models.CharField("title", max_length=255, blank=True)
    description = models.TextField("description", blank=True)
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
    change_freq = models.CharField("changefreq", max_length=7, choices=CHANGE_FREQ_CHOICES, default="yearly")
    priority = models.DecimalField(
        "priority",
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("0.1")), MaxValueValidator(Decimal("1.0"))],
        default=1.0,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name = "метаданные для страницы"
        verbose_name_plural = "метаданные для страниц"

    def generate_title(self):
        self.title = self.entity.name

    def generate_description(self):
        self.description = self.entity.name


class StaticPageMetadata(AbstractPageMetadata):
    entity = models.OneToOneField(Page, related_name="metadata", on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, related_name="static", on_delete=models.PROTECT, default=1)


class PostPageMetadata(AbstractPageMetadata):
    entity = models.OneToOneField(Post, related_name="metadata", on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, related_name="posts", on_delete=models.PROTECT, default=1)


class ProductPageMetadata(MetaGenerationRuleMixin, AbstractPageMetadata):
    entity = models.OneToOneField(Product, related_name="metadata", on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, related_name="products", on_delete=models.PROTECT, default=1)
    rule = models.ForeignKey(MetaGenerationRule, on_delete=models.RESTRICT, default="prd")


class CategoryGroupPageMetadata(MetaGenerationRuleMixin, AbstractPageMetadata):
    entity = models.OneToOneField(ProductCategoryGroup, related_name="metadata", on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, related_name="groups", on_delete=models.PROTECT, default=1)
    rule = models.ForeignKey(MetaGenerationRule, on_delete=models.RESTRICT, default="grp")


class CategoryPageMetadata(MetaGenerationRuleMixin, AbstractPageMetadata):
    entity = models.OneToOneField(ProductCategory, related_name="metadata", on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, related_name="categories", on_delete=models.PROTECT, default=1)
    rule = models.ForeignKey(MetaGenerationRule, on_delete=models.RESTRICT, default="ctg")
