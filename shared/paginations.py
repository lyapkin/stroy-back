import math
from rest_framework import pagination, exceptions
from rest_framework.response import Response


class BasePagination(pagination.PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        if hasattr(self, "page") and self.page is not None:
            response = super().get_paginated_response(data)
            response.data["pages"] = math.ceil(response.data["count"] / self.get_page_size(self.request))
            if response.data["next"] == None:
                del response.data["next"]
            if response.data["previous"] == None:
                del response.data["previous"]
            return response
        else:
            return Response(
                {
                    "count": 0,
                    "next": None,
                    "previous": None,
                    "results": data,
                }
            )

    def get_next_link(self):
        return self.page.next_page_number() if self.page.has_next() else None

    def get_previous_link(self):
        return self.page.previous_page_number() if self.page.has_previous() else None

    def paginate_queryset(self, queryset, request, view=None):
        try:
            result = super().paginate_queryset(queryset, request, view)
            return result
        except exceptions.NotFound:
            return list()
