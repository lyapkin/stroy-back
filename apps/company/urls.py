from django.urls import path, include
from rest_framework import routers

from .views import ContactsApi, RequisitesApi

router = routers.SimpleRouter(trailing_slash=True)
router.register("contacts", ContactsApi, basename="contact")
router.register("requisites", RequisitesApi, basename="requisite")


urlpatterns = [
    path("", include(router.urls)),
]
