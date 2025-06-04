from django.contrib import admin


class SlugNotRequiredAdminMixin(admin.ModelAdmin):

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["slug"].required = False
        return form
