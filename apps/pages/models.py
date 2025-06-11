from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Page(models.Model):
    name = models.CharField("страница", max_length=255, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    title = models.CharField("заголовок страницы", max_length=88)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"


class Content(models.Model):
    name = models.CharField("страница", max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    content = CKEditor5Field("контент", config_name="content")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "содержание страницы"
        verbose_name_plural = "содержание страниц"
