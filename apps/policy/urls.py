from django.urls import path, include
from rest_framework import routers

from .views import PolicyApi

router = routers.SimpleRouter(trailing_slash=True)
router.register("", PolicyApi, basename="policy")


urlpatterns = [
    path("", include(router.urls)),
]
