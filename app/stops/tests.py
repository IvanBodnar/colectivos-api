from django.db import connection
from django.test import TestCase

from .models import Stop
from .geo_fns import point_4326_to_98334


query_insert_98334 = '''
    INSERT into spatial_ref_sys
    (srid, auth_name, auth_srid, proj4text, srtext)
    values ( 98334, 'sr-org', 8333,
    '+proj=tmerc +lat_0=-34.6297166 +lon_0=-58.4627 +k=1 +x_0=100000 +y_0=100000 +ellps=intl +units=m +towgs84=-148,136,90,0,0,0,0 +no_defs ',
    'PROJCS["Gauss Krugger BA",
    GEOGCS["GCS_Campo_Inchauspe",
    DATUM["D_Campo_Inchauspe",
    SPHEROID["International_1924",6378388.0,297.0]],
    TOWGS84[-148,136,90,0,0,0,0],
     PRIMEM["Greenwich",0.0],
     UNIT["Degree",0.0174532925199433]],
     PROJECTION["Transverse_Mercator"],
     PARAMETER["False_Easting",100000.0],
     PARAMETER["False_Northing",100000.0],
     PARAMETER["Central_Meridian",-58.4627],
     PARAMETER["Scale_Factor",1.0],
     PARAMETER["Latitude_Of_Origin",-34.6297166],
     UNIT["Meter",1.0]]');
'''

query_populate_98334_column = '''
    update stops s
    set geom_98334 = st_transform(st_setsrid(st_makepoint(s.x, s.y), 4326), 98334)
    from (select id, x, y from stops) as xy
    where s.id = xy.id;
'''


class StopTests(TestCase):

    def setUp(self):
        Stop.objects.create(calle='test', numero=111, lineas='{1}', metrobus='f', x=1.0, y=2.0)
        Stop.objects.create(calle='test1', lineas='{1}', metrobus='f', stop_desc='cabildo av.&&ramallo', x=1.0, y=2.0)
        Stop.objects.create(
            calle='test_radius2',
            numero=111,
            lineas='{1}',
            metrobus='f',
            x=-58.4829388571869,
            y=-34.6340773094
        )
        Stop.objects.create(
            calle='test_radius3',
            numero=111,
            lineas='{1}',
            metrobus='f',
            x=-58.4841862230417,
            y=-34.634378796
        )

        with connection.cursor() as cursor:
            cursor.execute(query_insert_98334)
            cursor.execute(query_populate_98334_column)

    def test_get_stop_location(self):
        stop = Stop.objects.get(calle='test')
        stop1 = Stop.objects.get(calle='test1')
        self.assertEqual(stop.location, 'test 111')
        self.assertEqual(stop1.location, 'cabildo av. y ramallo')

    def test_str(self):
        stop = Stop.objects.get(calle='test')
        self.assertEqual(str(stop), f'Location: test 111 | id: {stop.id}')

    def test_radius_filter(self):
        stop_inside_radius = Stop.objects.get(calle='test_radius2')
        stop_outside_radius = Stop.objects.get(calle='test_radius3')

        filter1 = Stop.objects.radius_filter(x=-58.4832767076375, y=-34.6341590161, radius=83)
        filter2 = Stop.objects.radius_filter(x=-58.4832767076375, y=-34.6341590161, radius=86.8)
        filter3 = Stop.objects.radius_filter(x=-58.4832767076375, y=-34.6341590161, radius=87)

        self.assertIn(stop_inside_radius, filter1)
        self.assertIn(stop_inside_radius, filter2)
        self.assertIn(stop_inside_radius, filter3)
        self.assertNotIn(stop_outside_radius, filter1)
        self.assertNotIn(stop_outside_radius, filter2)
        self.assertIn(stop_outside_radius, filter3)


class GeoFnsTests(TestCase):

    def test_point_4326_to_98334(self):
        x = -58.486159
        y = -34.659705
        self.assertEqual(point_4326_to_98334(x, y).tuple, (97904.64416263279, 96623.46773679997))
