import random
from shapely.geometry import Point
import geopandas as gpd

def generate_random_points(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if random_point.within(polygon):  # Check if point is within the polygon
            points.append(random_point)
    return points

def extract_lon_lat(points):
    return [(point.x, point.y) for point in points]