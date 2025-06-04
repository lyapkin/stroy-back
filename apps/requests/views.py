from rest_framework import viewsets, mixins, response
from .models import CommercialRequest, ConsultationRequest, OrderRequest
from .serializers import CommercialRequestSerializer, ConsultationRequestSerializer, OrderReqeustSerializer


# Create your views here.
class CommercialRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CommercialRequest.objects.all()
    serializer_class = CommercialRequestSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)


class ConsultaionReqeustApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)


class OrderRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderReqeustSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)
