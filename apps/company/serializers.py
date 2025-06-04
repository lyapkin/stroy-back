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
        )


class ContactSerializer(serializers.ModelSerializer):
    phones = AdditioanlPhoneSerializer(many=True)
    emails = AdditioanlEmailSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Contact
        fields = (
            "email",
            "phone",
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
