"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.metadata.views import robots

urlpatterns = [
    path("robots.txt", robots),
    path("admin/", admin.site.urls),
    path("ck_upload/", include("shared.urls"), name="custom_ck_upload"),
    path("_nested_admin/", include("nested_admin.urls")),
    path("api/catalog/", include("apps.catalog.urls")),
    path("api/blog/", include("apps.blog.urls")),
    path("api/company/", include("apps.company.urls")),
    path("api/requests/", include("apps.requests.urls")),
    path("api/pages/", include("apps.pages.urls")),
    path("api/metadata/", include("apps.metadata.urls")),
    # path("api/policy/", include("apps.policy.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
