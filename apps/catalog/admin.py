from django.contrib import admin
import nested_admin
from apps.metadata.admin import ProductMetadataInline, CategoryGroupMetadataInline, CategoryMetadataInline
from apps.metadata.mixins import MetaGenrationActionMixin
from .models import (
    ProductCategoryGroup,
    ProductCategory,
    ProductImg,
    ProductDoc,
    ProductAttribute,
    Attribute,
    Product,
    AttributeValue,
    ProductPrice,
    ProductRedirectFrom,
    ProductCategoryRedirectFrom,
    ProductCategoryGroupRedirectFrom,
)


# Register your models here.
class ProductCategoryGroupRedirectFromInline(admin.TabularInline):
    model = ProductCategoryGroupRedirectFrom
    extra = 1


@admin.register(ProductCategoryGroup)
class ProductCategoryGroupAdmin(admin.ModelAdmin, MetaGenrationActionMixin):
    actions = ("generate_metadata",)
    fields = (
        "name",
        "slug",
        "image",
        "order",
        "description",
    )
    prepopulated_fields = {"slug": ["name"]}
    inlines = (
        CategoryGroupMetadataInline,
        ProductCategoryGroupRedirectFromInline,
    )

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["image"].required = False
        return form


class AtributeValueInine(nested_admin.NestedTabularInline):
    model = AttributeValue
    extra = 0
    verbose_name = "значение"
    verbose_name_plural = "возможные значения"


class AttributeInline(nested_admin.NestedTabularInline):
    model = Attribute
    inlines = (AtributeValueInine,)
    extra = 0


class ProductCategoryredirectFromInline(nested_admin.NestedInlineModelAdminMixin, admin.TabularInline):
    model = ProductCategoryRedirectFrom
    extra = 1


@admin.register(ProductCategory)
class ProductCatgeoryAdmin(nested_admin.NestedModelAdmin, MetaGenrationActionMixin):
    actions = ("generate_metadata",)
    fields = (
        "name",
        "slug",
        "group",
        "order",
        "description",
    )
    prepopulated_fields = {"slug": ["name"]}
    inlines = (
        AttributeInline,
        CategoryMetadataInline,
        ProductCategoryredirectFromInline,
    )

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["group"].widget.can_delete_related = False
        form.base_fields["group"].widget.can_change_related = False
        return form

    class Media:
        css = {"all": ("css/catalog/nested_inline.css",)}


class ImgInline(admin.TabularInline):
    model = ProductImg
    min_num = 1
    max_num = 0
    extra = 0
    fields = ("url", "order")
    template = "admin/image_inline.html"

    class Media:
        js = ("js/admin/add_img_to_list.js",)


class DocInline(admin.TabularInline):
    model = ProductDoc


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute

    def get_formset(self, request, obj=None, **kwargs):
        fs = super().get_formset(request, obj, **kwargs)
        fs.form.base_fields["value"].widget.can_add_related = False
        fs.form.base_fields["value"].widget.can_change_related = False
        fs.form.base_fields["value"].widget.can_view_related = False
        fs.form.base_fields["attribute"].widget.can_delete_related = False

        if obj:
            fs.form.base_fields["attribute"].queryset = obj.categories.all()[0].attributes.all()

        return fs

    class Media:
        js = (
            "product/js/admin/product_category_attribute_change.js",
            "product/js/admin/product_category_attribute_value_change.js",
        )


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    min_num = 1
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        formset.default_error_messages["too_few_forms"] = "Должна быть минимум одна цена"
        if obj:
            formset.default_error_messages["too_few_forms"] = (
                'Должна быть минимум одна цена (Возможно, вы пытаетесь удалить единственную цену - уберите галочку "удалить")'
            )
        return formset


class ProductRedirectFromInline(admin.TabularInline):
    model = ProductRedirectFrom
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, MetaGenrationActionMixin):
    actions = ("generate_metadata",)
    fields = [
        "hidden",
        "name",
        "slug",
        "categories",
        "stock",
        "best_price",
        "remainder",
        "description",
        "order",
    ]
    filter_horizontal = ("categories",)
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name"]
    inlines = (
        ProductPriceInline,
        ProductAttributeInline,
        ImgInline,
        DocInline,
        ProductMetadataInline,
        ProductRedirectFromInline,
    )
    ordering = ["name"]

    # def get_readonly_fields(self, request, obj=...):
    #     if obj:
    #         return ["category"]
    #     return super().get_readonly_fields(request, obj)
