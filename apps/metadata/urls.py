from django.urls import path, include
from rest_framework import routers


from .views import SitemapApi

router = routers.SimpleRouter(trailing_slash=True)
router.register("sitemap", SitemapApi)

urlpatterns = [
    path("", include(router.urls)),
]
