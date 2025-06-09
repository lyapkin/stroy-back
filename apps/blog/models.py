from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from shared.utils import post_preview_upload_to


class CategoryAbstract(models.Model):
    name = models.CharField("название", max_length=24, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# post
class PostCategory(CategoryAbstract):

    class Meta:
        verbose_name = "блог категория"
        verbose_name_plural = "блог категории"


class Post(models.Model):
    name = models.CharField("заголовок", max_length=112, unique=True)
    slug = models.SlugField("url (slug)", max_length=128, unique=True)
    categories = models.ManyToManyField(PostCategory, related_name="posts", verbose_name="категории поста", blank=True)

    excerpt = models.TextField("краткое описание", max_length=128)
    preview = models.ImageField("изображение карточки поста", upload_to=post_preview_upload_to)

    content = CKEditor5Field("пост", config_name="post")

    created = models.DateField("дата создания", auto_now_add=True)
    updated = models.DateField("дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "блог пост"
        verbose_name_plural = "блог посты"
        ordering = (
            "-created",
            "-id",
        )


# faq
class FaqCategory(CategoryAbstract):

    class Meta:
        verbose_name = "FAQ категория"
        verbose_name_plural = "FAQ категории"


class Faq(models.Model):
    question = models.CharField("вопрос", max_length=255, unique=True)
    answer = CKEditor5Field("ответ", config_name="faq")
    categories = models.ManyToManyField(FaqCategory, related_name="faqs", verbose_name="категории", blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ (Часто задаваемый вопрос)"
        verbose_name_plural = "FAQ (Часто задаваемые вопросы)"
