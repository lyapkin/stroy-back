from django.urls import path, include
from rest_framework import routers

from .views import (
    ProductCategoryGroupApi,
    ProductCategoryApi,
    ProductApi,
    CartApi,
    AttributeApi,
    AdminAttributeApi,
)


category_router = routers.SimpleRouter(trailing_slash=True)
category_router.register("groups", ProductCategoryGroupApi)
category_router.register("categories", ProductCategoryApi)

attributes_router = routers.SimpleRouter(trailing_slash=True)
attributes_router.register("", AttributeApi)

product_router = routers.SimpleRouter(trailing_slash=True)
product_router.register("products", ProductApi, basename="product")
product_router.register("cart", CartApi, basename="cart")

admin_router = routers.SimpleRouter(trailing_slash=True)
admin_router.register("attrs", AdminAttributeApi)


urlpatterns = [
    path("admin/", include(admin_router.urls)),
    path("", include(category_router.urls)),
    path("", include(product_router.urls)),
    path("attributes/", include(attributes_router.urls)),
]
