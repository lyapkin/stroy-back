from rest_framework import serializers
from .models import (
    ProductCategory,
    ProductCategoryGroup,
    ProductImg,
    ProductDoc,
    ProductAttribute,
    Product,
    Attribute,
    AttributeValue,
)


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = (
            "id",
            "name",
            "slug",
        )


class ProductCategoryGroupSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True)

    class Meta:
        model = ProductCategoryGroup
        fields = (
            "id",
            "name",
            "slug",
            "image",
            "categories",
        )


class ProductCategoryGroupItemSerializer(serializers.ModelSerializer):

    class Meta(ProductCategorySerializer.Meta):
        fields = (
            "id",
            "name",
            "slug",
        )


class ProductCategoryItemSerializer(ProductCategorySerializer):
    parents = ProductCategoryGroupItemSerializer(many=True, source="group")

    class Meta(ProductCategorySerializer.Meta):
        fields = ProductCategorySerializer.Meta.fields + ("parents",)


# product
class ProductImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImg
        fields = (
            "id",
            "url",
        )


class ProductDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDoc
        fields = (
            "id",
            "url",
            "name",
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source="attribute.name")
    value = serializers.CharField(source="value.name")

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "attribute",
            "value",
        )


class ProductBaseSerialzier(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "stock",
            "price",
            "discount",
            "attributes",
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        return dict([(key, repr[key]) for key in repr if repr[key] is not None])


class ProductListSerializer(ProductBaseSerialzier):
    image = serializers.ImageField(source="first_image.url")

    class Meta(ProductBaseSerialzier.Meta):
        fields = ProductBaseSerialzier.Meta.fields + ("image",)


class ProductDetailSerializer(ProductBaseSerialzier):
    images = ProductImgSerializer(many=True)
    docs = ProductDocSerializer(many=True)
    # seo = ProductSEOSerializer()

    class Meta(ProductBaseSerialzier.Meta):
        fields = ProductBaseSerialzier.Meta.fields + (
            "description",
            "remainder",
            "images",
            "docs",
            # "seo",
        )


class ProductRemainderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="first_image.url")

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "remainder",
            "image",
        )


# attributes
class AttributeValueSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = AttributeValue
        fields = (
            "id",
            "name",
            "slug",
        )

    def get_slug(self, obj):
        return f"{obj.attribute.name}:{obj.name}"


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True)
    slug = serializers.CharField(source="name")

    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
            "slug",
            "values",
        )
