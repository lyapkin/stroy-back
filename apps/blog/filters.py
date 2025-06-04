from django_filters import rest_framework as filters
from .models import Post, PostCategory


class PostFilter(filters.FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        field_name="categories", to_field_name="id", lookup_expr="exact", queryset=PostCategory.objects.all()
    )

    class Meta:
        model = Post
        fields = ["category"]
