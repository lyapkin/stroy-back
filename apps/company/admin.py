from django.contrib import admin
from django import forms
from .models import Contact, Requisite, RequisiteItem, AdditionalPhone, AdditionalEmail, Address


# Register your models here.
class AdditionalBaseInline(admin.TabularInline):
    fields = (
        "caption",
        "value",
    )


class AdditionalPhoneInline(AdditionalBaseInline):
    model = AdditionalPhone
    verbose_name = "дополнительный номер"
    verbose_name_plural = "дополнительные номера"

    def get_formset(self, request, obj=..., **kwargs):
        fs = super().get_formset(request, obj, **kwargs)
        fs.form.base_fields["value"].widget = forms.TelInput()
        return fs


class AdditionalEmailInline(AdditionalBaseInline):
    model = AdditionalEmail

    verbose_name = "дополнительный email"
    verbose_name_plural = "дополнительные email"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fields = (
        "caption",
        "city",
        "address",
        "weekdays",
        "weekends",
        "phone",
        "coordinates",
    )

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["phone"].widget = forms.TelInput()
        form.base_fields["coordinates"].required = False
        return form

    class Media:
        js = ("js/admin/format_phone.js",)


@admin.register(Contact)
class ContactsAdmin(admin.ModelAdmin):
    fields = [
        "email",
        "phone",
        "tg_instruction",
        "tg",
        "wa_instruction",
        "wa",
    ]
    inlines = (AdditionalPhoneInline, AdditionalEmailInline)

    def tg_instruction(self, instance):
        return "Номер телефона через + (например, +79221113344) или никнейм (например, nickname)"

    tg_instruction.short_description = "Инструкция для Telegram"

    def wa_instruction(self, instance):
        return "Номер (например, 79221113344)"

    wa_instruction.short_description = "Инструкция для Whatsapp"

    def get_readonly_fields(self, request, obj=None):
        return [
            "tg_instruction",
            "wa_instruction",
        ]

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["phone"].widget = forms.TelInput()
        return form

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    class Media:
        js = ("js/admin/format_phone.js",)


class RequisiteItemInline(admin.TabularInline):
    model = RequisiteItem
    fields = (
        "name",
        "value",
    )


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    inlines = (RequisiteItemInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False
