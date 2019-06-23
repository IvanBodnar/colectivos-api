from django.contrib.gis.geos import Point


# The proj4 definition must be added because
# django doesn't seem to be able to pick it up
# from spatial_ref_sys.
proj4_98334 = '''
    +proj=tmerc +lat_0=-34.6297166 +lon_0=-58.4627 +k=1
    +x_0=100000 +y_0=100000 +ellps=intl +units=m
    +towgs84=-148,136,90,0,0,0,0 +no_defs
'''


def point_4326_to_98334(x: float, y: float) -> Point:
    point = Point(x, y, srid=4326)
    point.transform(proj4_98334)
    return point
