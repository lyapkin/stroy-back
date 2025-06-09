from rest_framework import viewsets, mixins
from .models import Page
from .serializers import PageSerializer


# Create your views here.
class PageApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"
