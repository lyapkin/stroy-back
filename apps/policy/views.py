from rest_framework import viewsets, mixins
from .models import Policy
from .serializers import PolicySerializer


# Create your views here.
class PolicyApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    lookup_field = "slug"
