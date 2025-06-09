from rest_framework import viewsets, mixins
from .models import Page, Content
from .serializers import PageSerializer, ContentSerializer


# Create your views here.
class PageApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"


class ContentApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "slug"
