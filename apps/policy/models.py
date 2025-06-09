from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Policy(models.Model):
    name = models.CharField("название", max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    content = CKEditor5Field("контент", config_name="policy")

    class Meta:
        verbose_name = "условие"
        verbose_name_plural = "условия"

    def __str__(self):
        return self.name
