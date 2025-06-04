from rest_framework import serializers
from shared.serializers import CKEditorFieldWithMediaSerializer
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


class PostDetailSerializer(serializers.ModelSerializer):
    content = CKEditorFieldWithMediaSerializer()
    # seo = PostSEOSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "content",
            # "seo",
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
