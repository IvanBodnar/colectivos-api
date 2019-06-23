from rest_framework import viewsets, mixins

from .models import Stop
from .serializers import StopSerializer


class StopViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
