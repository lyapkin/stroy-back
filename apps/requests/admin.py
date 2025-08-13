from django.contrib import admin
from .models import CommercialRequest, OrderRequest, OrderRequestItem, ConsultationRequest


# Register your models here.
@admin.register(CommercialRequest)
class CommercialRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "date"]
    readonly_fields = (
        "file",
        "date",
        "comment",
        "addition",
    )


class OrderRequestItem(admin.TabularInline):
    model = OrderRequestItem

    def has_change_permission(self, request, obj=...):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request, obj=...):
        return False


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "date"]
    readonly_fields = (
        "date",
        "comment",
        "addition",
    )
    inlines = (OrderRequestItem,)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "date"]
    readonly_fields = (
        "date",
        "comment",
        "addition",
    )
