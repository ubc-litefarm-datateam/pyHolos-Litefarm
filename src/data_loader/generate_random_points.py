"""
This module includes functions to generate random points that 
fall within a specified polygon and to extract geographic 
coordinates (longitude and latitude) from a list of points.

Functions
---------
generate_random_points(polygon, num_points)
    Generates a specified number of random points within the 
    bounds of a given polygon.

extract_lon_lat(points)
    Extracts and returns the longitude and latitude from a list 
    of Shapely Point objects as tuples of (longitude, latitude).

Examples
--------
>>> from shapely.geometry import Polygon
>>> test_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
>>> random_points = generate_random_points(test_polygon, 5)
>>> coords = extract_lon_lat(random_points)
"""

import random
from shapely.geometry import Point, Polygon


def generate_random_points(polygon, num_points):
    """Generate random points within a specified polygon.

    This function creates random points within the bounds of the
    polygon until the desired number of points is reached.

    Parameters
    ----------
    polygon: shapely.geometry.Polygon
        The polygon within which to generate random points.
    num_points: int
        The number of random points to generate within the polygon.

    Returns
    ----------
    list of shapely.geometry.Point
        A list of points that are within the given polygon.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> test_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    >>> generate_random_points(test_polygon, 5)
    """
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point(
            [random.uniform(min_x, max_x), random.uniform(min_y, max_y)]
        )
        if random_point.within(polygon):  # Check if point is within the polygon
            points.append(random_point)
    return points


def extract_lon_lat(points):
    """
    Extract longitude and latitude from a list of points.

    Parameters
    ----------
    points : list of shapely.geometry.Point
        The points from which to extract longitude and latitude.

    Returns
    ----------
    list of tuples
        A list of (longitude, latitude) tuples for each point.

    Examples
    --------
    >>> points = [Point(1, 2), Point(3, 4)]
    >>> extract_lon_lat(points)
    """
    return [(point.x, point.y) for point in points]


if __name__ == "__main__":
    # Define a polygon using coordinates that form a simple square
    test_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    # Generate 5 random points within the polygon
    random_points = generate_random_points(test_polygon, 5)

    # Extract the longitude and latitude from these points
    coordinates = extract_lon_lat(random_points)

    # Print out the coordinates of each point
    print("Generated Coordinates:")
    for coord in coordinates:
        print(f"Longitude: {coord[0]}, Latitude: {coord[1]}")
