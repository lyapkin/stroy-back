from django.db import models


# Create your models here.
class Page(models.Model):
    name = models.CharField("страница", max_length=255, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    title = models.CharField("заголовок страницы", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"
