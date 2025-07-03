from rest_framework import serializers
from .models import Contact, Requisite, RequisiteItem, AdditionalPhone, AdditionalEmail, Address


class AdditionalBaseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "caption",
            "value",
        )


class AdditioanlPhoneSerializer(AdditionalBaseSerializer):

    class Meta(AdditionalBaseSerializer.Meta):
        model = AdditionalPhone


class AdditioanlEmailSerializer(AdditionalBaseSerializer):

    class Meta(AdditionalBaseSerializer.Meta):
        model = AdditionalEmail


class AddressSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = (
            "id",
            "city",
            "address",
            "caption",
            "weekdays",
            "weekends",
            "phone",
            "coordinates",
        )

    def get_coordinates(self, obj):
        if obj.coordinates is None:
            return None

        arr = obj.coordinates.split(", ")
        if len(arr) != 2:
            return None
        try:
            result = list(map(lambda item: float(item), arr))
            result.reverse()
            return result
        except:
            return None


class ContactSerializer(serializers.ModelSerializer):
    phones = AdditioanlPhoneSerializer(many=True)
    emails = AdditioanlEmailSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Contact
        fields = (
            "email",
            "phone",
            "phone2",
            "tg",
            "wa",
            "phones",
            "emails",
            "addresses",
        )


# requisites
class RequisiteItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequisiteItem
        fields = ("id", "name", "value")


class RequisitesSerializer(serializers.ModelSerializer):
    requisites = RequisiteItemSerializer(many=True)

    class Meta:
        model = Requisite
        fields = (
            "name",
            "requisites",
        )
