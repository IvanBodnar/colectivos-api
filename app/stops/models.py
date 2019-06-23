from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.contrib.postgres.fields import ArrayField
from django.db.models.query import QuerySet

from .geo_fns import point_4326_to_98334


class StopManager(models.Manager):
    """
    Adds method to default Manager for Stop model.
    """
    def radius_filter(self, x: float, y: float, radius: float) -> QuerySet:
        """
        Makes a Point object out of the x and y WGS84 coordinates,
        transforms it to 98334, and filters the Stop objects by
        distance, fetching the ones that are at the radius distance
        or less.
        :param x: longitude
        :param y: latitude
        :param radius: radius in meters
        :return: QuerySet
        """
        center_point = point_4326_to_98334(x, y)
        distance_obj = D(m=radius)
        return self.model.objects.filter(geom_98334__distance_lte=(center_point, distance_obj))


class Stop(models.Model):
    """
    Represents a bus stop
    """
    tipo = models.CharField(max_length=255, null=True)
    calle = models.CharField(max_length=255, null=True)
    numero = models.IntegerField(null=True)
    entre1 = models.CharField(max_length=255, null=True)
    entre2 = models.CharField(max_length=255, null=True)
    lineas = ArrayField(base_field=models.IntegerField())
    dir_norm = models.CharField(max_length=255, null=True)
    metrobus = models.BooleanField()
    stop_desc = models.CharField(max_length=255, null=True)
    x = models.FloatField()
    y = models.FloatField()
    geom = models.PointField(null=True)
    geom_98334 = models.PointField(srid=98334, null=True)

    objects = StopManager()

    @property
    def location(self) -> str:
        if self.calle and self.numero:
            name = f'{self.calle} {self.numero}'
        elif self.stop_desc:
            name = str(self.stop_desc).replace('&&', ' y ')
        else:
            name = 'no name assigned'
        return name

    class Meta:
        db_table = 'stops'

    def __str__(self) -> str:
        return f'Location: {self.location} | id: {self.id}'
