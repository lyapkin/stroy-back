from django import get_version
from django.views.decorators.http import require_POST

from django_ckeditor_5.exceptions import NoImageException
from django_ckeditor_5.permissions import check_upload_permission
from django_ckeditor_5.storage_utils import image_verify, handle_uploaded_file

if get_version() >= "4.0":
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.http import JsonResponse

from django_ckeditor_5.forms import UploadFileForm


@require_POST
@check_upload_permission
def upload_file(request):
    path = request.META["HTTP_REFERER"].split("/")
    start = path.index("admin") + 1
    end = start + 3
    path = path[start:end]

    form = UploadFileForm(request.POST, request.FILES)
    allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES", False)

    if not allow_all_file_types:
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)

    if form.is_valid():
        f = request.FILES["upload"]
        setattr(f, "path", path)
        url = handle_uploaded_file(f)
        return JsonResponse({"url": url})

    if form.errors["upload"]:
        return JsonResponse(
            {"error": {"message": form.errors["upload"][0]}},
            status=400,
        )

    return JsonResponse({"error": {"message": _("Invalid form data")}}, status=400)
