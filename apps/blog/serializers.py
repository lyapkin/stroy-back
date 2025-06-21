from rest_framework import serializers
from shared.serializers import CKEditorFieldWithMediaSerializer
from apps.metadata.serializers import PostMetadataSerializer
from .models import PostCategory, Post, FaqCategory, Faq


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "slug",
            "excerpt",
            "preview",
        )


class VideoField(serializers.URLField):
    FIRST_SEARCH_PATTERN = "_"
    FIRST_REPLACE_WITH = "&id="

    SECOND_SEARCH_PATTERN = "video-"
    SECOND_REPLACE_WITH = "video_ext.php?oid=-"

    def to_representation(self, value):
        value = super().to_representation(value)
        value = value.replace(self.FIRST_SEARCH_PATTERN, self.FIRST_REPLACE_WITH)
        value = value.replace(self.SECOND_SEARCH_PATTERN, self.SECOND_REPLACE_WITH)
        return value


class PostDetailSerializer(serializers.ModelSerializer):
    video = VideoField()
    content = CKEditorFieldWithMediaSerializer()
    metadata = PostMetadataSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "video",
            "content",
            "metadata",
        )


class PostCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCategory
        fields = (
            "id",
            "name",
        )


# faq
class FaqCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqCategory
        fields = (
            "id",
            "name",
        )


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = (
            "id",
            "question",
            "answer",
            "categories",
        )
