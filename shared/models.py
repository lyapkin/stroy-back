from django.db import models
from .utils import generate_unique_slug


# Create your models here.
# class AbstractGenerateSlugModel(models.Model):

#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         if not self.slug.strip():
#             self.slug = generate_unique_slug(self._meta.model, self.get_base_for_slug())
#         return super().save(*args, **kwargs)

#     def get_base_for_slug(self):
#         if self.name and isinstance(self.name, str):
#             return self.name
#         raise NotImplementedError(
#             'If there isn\'t the "name" field as the "str" type, a "get_base_for_slug" method must be implemented'
#         )
