from django.urls import path

from .views import upload_file

urlpatterns = [
    path("file_upload/", upload_file, name="custom_upload_file"),
]
