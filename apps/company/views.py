from rest_framework import viewsets, mixins
from .models import Contact, Requisite
from .serializers import ContactSerializer, RequisitesSerializer


# Create your views here.
class ContactsApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Contact.objects.all().prefetch_related("addresses", "emails", "phones")
    serializer_class = ContactSerializer


class RequisitesApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Requisite.objects.all().prefetch_related("requisites")
    serializer_class = RequisitesSerializer
