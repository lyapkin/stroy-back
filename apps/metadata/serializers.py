from rest_framework import serializers
from .models import (
    Sitemap,
    StaticPageMetadata,
    ProductPageMetadata,
    CategoryGroupPageMetadata,
    CategoryPageMetadata,
    PostPageMetadata,
)


# metadata
class MetadataSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "title",
            "description",
            "noindex_follow",
            "change_freq",
            "priority",
        )


class StaticMetadataSerializer(MetadataSerializer):

    class Meta(MetadataSerializer.Meta):
        model = StaticPageMetadata


class ProductMetadataSerializer(MetadataSerializer):

    class Meta(MetadataSerializer.Meta):
        model = ProductPageMetadata


class CategoryGroupMetadataSerializer(MetadataSerializer):

    class Meta(MetadataSerializer.Meta):
        model = CategoryGroupPageMetadata


class CategoryMetadataSerializer(MetadataSerializer):

    class Meta(MetadataSerializer.Meta):
        model = CategoryPageMetadata


class PostMetadataSerializer(MetadataSerializer):

    class Meta(MetadataSerializer.Meta):
        model = PostPageMetadata


# sitemap
class SitemapEntitySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(source="entity.slug")

    class Meta:
        fields = (
            "slug",
            "priority",
            "change_freq",
        )


class SitemapPageSerializer(SitemapEntitySerializer):

    class Meta(SitemapEntitySerializer.Meta):
        model = StaticPageMetadata


class SitemapProductSerializer(SitemapEntitySerializer):

    class Meta(SitemapEntitySerializer.Meta):
        model = ProductPageMetadata


class SitemapCategoryGroupSerializer(SitemapEntitySerializer):

    class Meta(SitemapEntitySerializer.Meta):
        model = CategoryGroupPageMetadata


class SitemapCategorySerializer(SitemapEntitySerializer):
    slug = serializers.SerializerMethodField(method_name="get_slug")

    class Meta(SitemapEntitySerializer.Meta):
        model = CategoryPageMetadata

    def get_slug(self, obj):
        return f"{obj.entity.group.slug}/{obj.entity.slug}"


class SitemapPostSerializer(SitemapEntitySerializer):

    class Meta(SitemapEntitySerializer.Meta):
        model = PostPageMetadata


class SitemapSerializer(serializers.ModelSerializer):
    static = SitemapPageSerializer(many=True)
    products = SitemapProductSerializer(many=True)
    groups = SitemapCategoryGroupSerializer(many=True)
    categories = SitemapCategorySerializer(many=True)
    posts = SitemapPostSerializer(many=True)

    class Meta:
        model = Sitemap
        exclude = ("id",)
