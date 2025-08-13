import re
from rest_framework import serializers
from shared.utils import calculate_item_price
from .models import CommercialRequest, OrderRequest, OrderRequestItem, ConsultationRequest


class BaseRequestSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "name",
            "phone",
            "comment",
            "addition",
        )

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_phone(self, number):
        result = re.match(r"^\+\d{9,19}$", number) or re.match(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", number)
        if result is None:
            raise serializers.ValidationError("Номер телефона указан неверно")

        return number


class CommercialRequestSerializer(BaseRequestSerializer):

    class Meta(BaseRequestSerializer.Meta):
        model = CommercialRequest
        fields = BaseRequestSerializer.Meta.fields + ("file",)


# consultation
class ConsultationRequestSerializer(BaseRequestSerializer):

    class Meta(BaseRequestSerializer.Meta):
        model = ConsultationRequest


# order
class OrderRequestItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderRequestItem
        fields = (
            "variant",
            "quantity",
        )


class OrderReqeustSerializer(BaseRequestSerializer):
    items = OrderRequestItemSerializer(many=True)

    class Meta(BaseRequestSerializer.Meta):
        model = OrderRequest
        fields = BaseRequestSerializer.Meta.fields + ("items",)

    def create(self, validated_data):
        order_items = validated_data.pop("items")
        instance = OrderRequest.objects.create(**validated_data)
        order_items = list(
            map(
                lambda item: OrderRequestItem(
                    **item,
                    price=calculate_item_price(item["variant"].price, item["variant"].discount),
                    order=instance,
                    product=item["variant"].product,
                    variant_text=item["variant"].name
                ),
                order_items,
            )
        )
        OrderRequestItem.objects.bulk_create(order_items)
        return instance
