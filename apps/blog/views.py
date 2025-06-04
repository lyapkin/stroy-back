import math
from rest_framework import viewsets, mixins
from django_filters import rest_framework as django_filters
from shared.paginations import BasePagination
from .models import PostCategory, Post, Faq, FaqCategory
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCategorySerializer,
    FaqSerializer,
    FaqCategorySerializer,
)
from .filters import PostFilter


class PostCategoryApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostApi(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_action_classes = {"list": PostListSerializer, "retrieve": PostDetailSerializer}
    lookup_field = "slug"
    pagination_class = BasePagination
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


# faq
class FaqCategoryApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = FaqCategory.objects.all()
    serializer_class = FaqCategorySerializer


class FaqApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Faq.objects.prefetch_related("categories").all()
    serializer_class = FaqSerializer
