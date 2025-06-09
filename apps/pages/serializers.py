from rest_framework import serializers
from apps.metadata.serializers import StaticMetadataSerializer
from .models import Page, Content


class PageSerializer(serializers.ModelSerializer):
    metadata = StaticMetadataSerializer()

    class Meta:
        model = Page
        fields = (
            "id",
            "slug",
            "title",
            "metadata",
        )


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = (
            "id",
            "name",
            "content",
        )
