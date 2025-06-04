from rest_framework import serializers
from django.conf import settings


class CKEditorFieldWithMediaSerializer(serializers.Field):
    SEARCH_PATTERN = 'src="/media/'
    SITE_DOMAIN = "http://127.0.0.1:8000"
    REPLACE_WITH = 'src="%s/media/' % SITE_DOMAIN

    def to_representation(self, value):
        if settings.DEBUG:
            text = value.replace(self.SEARCH_PATTERN, self.REPLACE_WITH)
            return text
        return value
