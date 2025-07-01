from rest_framework import serializers
from apps.metadata.serializers import (
    ProductMetadataSerializer,
    CategoryGroupMetadataSerializer,
    CategoryMetadataSerializer,
)
from .models import (
    ProductCategory,
    ProductCategoryGroup,
    ProductImg,
    ProductDoc,
    ProductAttribute,
    Product,
    Attribute,
    AttributeValue,
    ProductPrice,
)


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = (
            "id",
            "name",
            "slug",
            "description",
        )


class ProductCategoryGroupSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True)
    metadata = CategoryGroupMetadataSerializer()

    class Meta:
        model = ProductCategoryGroup
        fields = (
            "id",
            "name",
            "slug",
            "image",
            "categories",
            "description",
            "metadata",
        )


class ProductCategoryGroupItemSerializer(serializers.ModelSerializer):

    class Meta(ProductCategorySerializer.Meta):
        fields = (
            "id",
            "name",
            "slug",
        )


class ProductCategoryItemSerializer(ProductCategorySerializer):
    parent = ProductCategoryGroupItemSerializer(source="group")
    metadata = CategoryMetadataSerializer()

    class Meta(ProductCategorySerializer.Meta):
        fields = ProductCategorySerializer.Meta.fields + (
            "parent",
            "metadata",
        )


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


class ProductPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPrice
        fields = (
            "id",
            "price",
            "discount",
            "name",
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
            "attributes",
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        return dict([(key, repr[key]) for key in repr if repr[key] is not None])


class ProductListSerializer(ProductBaseSerialzier):
    image = serializers.ImageField(source="first_image")
    price = serializers.SerializerMethodField()

    class Meta(ProductBaseSerialzier.Meta):
        fields = ProductBaseSerialzier.Meta.fields + (
            "image",
            "price",
        )

    def get_price(self, product):
        count = product.prices.count()
        price = product.prices.first()
        price_repr = ProductPriceSerializer(price).data
        if count > 1:
            price_repr.update({"single": False})
        else:
            price_repr.update({"single": True})

        return price_repr


class ProductDetailSerializer(ProductBaseSerialzier):
    images = ProductImgSerializer(many=True)
    docs = ProductDocSerializer(many=True)
    metadata = ProductMetadataSerializer()
    prices = ProductPriceSerializer(many=True)

    class Meta(ProductBaseSerialzier.Meta):
        fields = ProductBaseSerialzier.Meta.fields + (
            "description",
            "remainder",
            "images",
            "docs",
            "metadata",
            "prices",
        )


class ProductCartSerializer(ProductBaseSerialzier):
    image = serializers.ImageField(source="first_image")
    prices = ProductPriceSerializer(many=True)

    class Meta(ProductBaseSerialzier.Meta):
        fields = ProductBaseSerialzier.Meta.fields + (
            "image",
            "prices",
        )


class ProductRemainderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="first_image")

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
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
