from django.contrib import admin
from nested_admin import nested
from .models import (
    Robots,
    MetaGenerationRule,
    StaticPageMetadata,
    ProductPageMetadata,
    CategoryGroupPageMetadata,
    CategoryPageMetadata,
    PostPageMetadata,
)
from .forms import MetadataInlineFormModel


# Register your models here.
@admin.register(Robots)
class RobotsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MetaGenerationRule)
class MetaGenerationRuleAdmin(admin.ModelAdmin):
    fields = [
        "type",
        "instruction",
        "title",
        "description",
    ]

    def instruction(self, instance):
        return """Для генерации можно использовать переменные, название которых заключается в фигурные скобки {} (например, {name}).
                  Доступные переменные:
                  {name} - название"""

    instruction.short_description = "Инструкция"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "type",
                "instruction",
            ]
        else:
            return []

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MetadataInline(admin.StackedInline):
    fieldsets = (
        (None, {"fields": ["title", "description", "noindex_follow"]}),
        (
            "Sitemap",
            {
                "fields": ("change_freq", "priority"),
            },
        ),
    )
    can_delete = False
    form = MetadataInlineFormModel
    max_num = 1
    min_num = 1


class StaticMetadataInline(MetadataInline):
    model = StaticPageMetadata


class ProductMetadataInline(MetadataInline):
    model = ProductPageMetadata


class CategoryGroupMetadataInline(MetadataInline):
    model = CategoryGroupPageMetadata


class CategoryMetadataInline(nested.NestedInlineModelAdminMixin, MetadataInline):
    model = CategoryPageMetadata


class PostMetadataInline(MetadataInline):
    model = PostPageMetadata
