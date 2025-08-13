from rest_framework import viewsets, mixins, response
from .models import CommercialRequest, ConsultationRequest, OrderRequest
from .serializers import CommercialRequestSerializer, ConsultationRequestSerializer, OrderReqeustSerializer
from .utils import send_email_notification


# Create your views here.
class CommercialRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CommercialRequest.objects.all()
    serializer_class = CommercialRequestSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)

    def perform_create(self, serializer):
        super().perform_create(serializer)

        instance = serializer.instance

        subject = "Запрос коммерческого предложения сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос коммерческого предложения сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
            f"Ссылка на файл: {instance.file and self.request.build_absolute_uri(instance.file.url)}"
            f"Комментарий: {instance.comment and instance.comment}"
            f"\n\n\nДоп. информация:\n\n{instance.addition}"
        )

        send_email_notification(subject, message)


class ConsultaionReqeustApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)

    def perform_create(self, serializer):
        super().perform_create(serializer)

        instance = serializer.instance

        subject = "Запрос консультации с сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос консультации с сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
            f"Комментарий: {instance.comment and instance.comment}"
            f"\n\n\nДоп. информация:\n\n{instance.addition}"
        )

        send_email_notification(subject, message)


class OrderRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderReqeustSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(None, status=res.status_code, headers=res.headers)

    def perform_create(self, serializer):
        super().perform_create(serializer)

        instance = serializer.instance

        subject = "Запрос из корзины сайта: " + instance.name + " - " + instance.phone
        message = (
            f"Запрос из корзины сайта.\n\n"
            f"Контактное лицо: {instance.name}\n" + f"Номер телефона: {instance.phone}\n"
            f"Комментарий: {instance.comment and instance.comment}\n"
            f"Товары:\n"
        )

        for item in instance.items.all():
            message = message + (
                f"\n\tНазвание товара: {item.product.name}\n"
                f"\tВариант товара: {item.variant_text}\n"
                f"\tКоличество: {item.quantity}\n"
                f"\tЦена на момент запроса (с учетом скидки, за единицу): {item.price}\n"
            )
        message = message + f"\n\n\nДоп. информация:\n\n{instance.addition}"
        print(message)

        send_email_notification(subject, message)
