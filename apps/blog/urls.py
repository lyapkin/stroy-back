from django.urls import path, include
from rest_framework import routers

from .views import PostApi, PostCategoryApi, FaqApi, FaqCategoryApi

blog_router = routers.SimpleRouter(trailing_slash=True)
blog_router.register("posts", PostApi)
blog_router.register("post-categories", PostCategoryApi)
blog_router.register("faqs", FaqApi)
blog_router.register("faq-categories", FaqCategoryApi)


urlpatterns = [
    path("", include(blog_router.urls)),
]
