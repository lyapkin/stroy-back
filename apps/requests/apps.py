from django.apps import AppConfig
from django.db.models.signals import post_save


class RequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.requests"
    verbose_name = "запросы"

    def ready(self):
        from .signals import request_notification
        from .models import ConsultationRequest, OrderRequest, CommercialRequest

        post_save.connect(
            request_notification.email_notification_on_call_request,
            sender=ConsultationRequest,
            weak=False,
            dispatch_uid="ConsultationRequestFromClient",
        )

        post_save.connect(
            request_notification.email_notification_on_order_request,
            sender=OrderRequest,
            weak=False,
            dispatch_uid="ConsultationRequestFromClient",
        )

        post_save.connect(
            request_notification.email_notification_on_commercial_request,
            sender=CommercialRequest,
            weak=False,
            dispatch_uid="ConsultationRequestFromClient",
        )
