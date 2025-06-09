from django.shortcuts import HttpResponse
from django.db.models import Prefetch
from rest_framework import viewsets, mixins
from .models import Robots, Sitemap
from .serializers import SitemapSerializer


# Create your views here.
def robots(req):
    robots = Robots.objects.all()[0]
    return HttpResponse(robots.text, content_type="text/plain")


class SitemapApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Sitemap.objects.all()
    serializer_class = SitemapSerializer

    def get_object(self):
        return (
            self.get_queryset()
            .prefetch_related(
                "static",
                Prefetch(
                    "products",
                    queryset=Sitemap.products.rel.related_model.objects.select_related("entity"),
                ),
                Prefetch(
                    "groups",
                    queryset=Sitemap.groups.rel.related_model.objects.select_related("entity"),
                ),
                Prefetch(
                    "categories",
                    queryset=Sitemap.categories.rel.related_model.objects.select_related("entity__group"),
                ),
                Prefetch(
                    "posts",
                    queryset=Sitemap.posts.rel.related_model.objects.select_related("entity"),
                ),
            )
            .first()
        )
