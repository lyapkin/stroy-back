from rest_framework import serializers
from apps.metadata.serializers import StaticMetadataSerializer
from .models import Page


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
