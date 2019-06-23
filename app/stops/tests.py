from django.test import TestCase

from .models import Stop
from .geo_fns import point_4326_to_98334


class StopTests(TestCase):

    def setUp(self):
        Stop.objects.create(calle='test', numero=111, lineas='{1}', metrobus='f', x=1.0, y=2.0)
        Stop.objects.create(calle='test1', lineas='{1}', metrobus='f', stop_desc='cabildo av.&&ramallo', x=1.0, y=2.0)

    def test_get_stop_location(self):
        stop = Stop.objects.get(calle='test')
        stop1 = Stop.objects.get(calle='test1')
        self.assertEqual(stop.location, 'test 111')
        self.assertEqual(stop1.location, 'cabildo av. y ramallo')

    def test_str(self):
        stop = Stop.objects.get(calle='test')
        self.assertEqual(str(stop), f'Location: test 111 | id: {stop.id}')


class GeoFnsTests(TestCase):

    def test_point_4326_to_98334(self):
        x = -58.486159
        y = -34.659705
        self.assertEqual(point_4326_to_98334(x, y).tuple, (97904.64416263279, 96623.46773679997))
