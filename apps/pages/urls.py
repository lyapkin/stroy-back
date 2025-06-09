from django.urls import path, include
from rest_framework import routers

from .views import PageApi

router = routers.SimpleRouter(trailing_slash=True)
router.register("static", PageApi, basename="page")


urlpatterns = [
    path("", include(router.urls)),
]
