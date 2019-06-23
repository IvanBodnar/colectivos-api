from rest_framework.generics import ListAPIView

from .models import Stop
from .serializers import StopSerializer


class StopListView(ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
