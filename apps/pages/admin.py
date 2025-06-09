from django.contrib import admin
from apps.metadata.admin import StaticMetadataInline
from .models import Page


# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = [
        "name",
        "new_line_instruction",
    ]
    inlines = (StaticMetadataInline,)

    def new_line_instruction(self, instance):
        return """Для разбивки заголовка страницы на несколько строк, следует вставить "<br>" в месте разбивки (нарпимер, "Производство и поставка<br>комплектующих для<br>строительных объектов") """

    new_line_instruction.short_description = "Инструкция"

    def get_fields(self, request, obj=...):
        if obj.slug == "home" or obj.slug == "about":
            return [
                "name",
                "new_line_instruction",
                "title",
            ]
        else:
            return [
                "name",
                "title",
            ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False
