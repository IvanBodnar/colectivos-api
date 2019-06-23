from rest_framework import serializers

from .models import Stop


class StopSerializer(serializers.ModelSerializer):
    location = serializers.ReadOnlyField()

    class Meta:
        model = Stop
        fields = ('id', 'tipo', 'location', 'lineas', 'x', 'y')
        read_only_fields = ('id',)
