from django.urls import path, include
from rest_framework import routers

from .views import CommercialRequestApi, OrderRequestApi, ConsultaionReqeustApi

router = routers.SimpleRouter(trailing_slash=True)
router.register("commercial", CommercialRequestApi)
router.register("order", OrderRequestApi)
router.register("consultation", ConsultaionReqeustApi)


urlpatterns = [
    path("", include(router.urls)),
]
