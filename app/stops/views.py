from rest_framework.generics import ListAPIView

from .models import Stop
from .serializers import StopSerializer


class StopListView(ListAPIView):
    serializer_class = StopSerializer

    def get_queryset(self):
        queryset = Stop.objects.all()
        x = self.request.query_params.get('x', None)
        y = self.request.query_params.get('y', None)
        radius = self.request.query_params.get('radius', None)
        if all((x, y, radius)):
            queryset = Stop.objects.radius_filter(float(x), float(y), float(radius))
        return queryset
