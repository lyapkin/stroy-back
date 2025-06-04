from django.contrib import admin
from shared.admin import SlugNotRequiredModelAdmin
from .models import Post, PostCategory, Faq, FaqCategory


# Register your models here.
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(SlugNotRequiredModelAdmin):
    fields = ["name", "slug", "categories", "excerpt", "preview", "content"]
    list_display = ["name", "updated", "created"]
    filter_horizontal = ("categories",)
    prepopulated_fields = {"slug": ["name"]}
    # inlines = (PostSEOInline,)

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["categories"].widget.can_delete_related = False
        form.base_fields["categories"].widget.can_change_related = False
        return form


# faq
@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ["question"]
    filter_horizontal = ("categories",)
