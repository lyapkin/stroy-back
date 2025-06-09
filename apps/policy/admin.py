from django.contrib import admin
from .models import Policy


# Register your models here.
@admin.register(Policy)
class ProductCatgeoryGroupAdmin(admin.ModelAdmin):
    fields = ("name", "content")
    readonly_fields = ["name"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False
