from django.urls import path

from .views import StopListView


urlpatterns = [
    path('', StopListView.as_view(), name='stops_list')
]
