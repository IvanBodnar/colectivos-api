from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Stop(models.Model):
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

    @property
    def location(self):
        if self.calle and self.numero:
            name = f'{self.calle} {self.numero}'
        elif self.stop_desc:
            name = str(self.stop_desc).replace('&&', ' y ')
        else:
            name = 'no name assigned'
        return name

    class Meta:
        db_table = 'stops'

    def __str__(self):
        return f'Location: {self.location} | id: {self.id}'
