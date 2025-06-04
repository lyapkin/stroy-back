from django.urls import path, include
from rest_framework import routers

from .views import category_attributes, attribute_values, ProductCategoryGroupApi, ProductApi, CartApi, AttributeApi


category_router = routers.SimpleRouter(trailing_slash=True)
category_router.register("groups", ProductCategoryGroupApi)
# category_router.register("categories", ProductCategoryApi)
# category_router.register("attributes", AttributeApi)

attributes_router = routers.SimpleRouter(trailing_slash=True)
attributes_router.register("", AttributeApi)

product_router = routers.SimpleRouter(trailing_slash=True)
product_router.register("products", ProductApi, basename="product")
product_router.register("cart", CartApi, basename="cart")


urlpatterns = [
    path("category-attributes/<int:id>/", category_attributes),
    path("attribute-values/<int:id>/", attribute_values),
    # path("", include(blog_router.urls)),
    path("", include(category_router.urls)),
    path("", include(product_router.urls)),
    path("attributes/<str:category_slug>/", include(attributes_router.urls)),
]
