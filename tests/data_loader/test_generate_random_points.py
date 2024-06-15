import pytest
from shapely.geometry import Polygon, Point
from src.data_loader.generate_random_points import (
    generate_random_points,
    extract_lon_lat,
)


def test_generate_random_points():
    """Test generating random points within a specified polygon."""
    test_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    num_points = 5
    points = generate_random_points(test_polygon, num_points)
    assert len(points) == num_points, "Incorrect number of points generated"
    all_within = all(point.within(test_polygon) for point in points)
    assert all_within, "Not all points are within the polygon"


def test_extract_lon_lat():
    """Test extracting longitude and latitude from a list of points."""
    points = [Point(1, 2), Point(3, 4)]
    expected_coords = [(1, 2), (3, 4)]
    coords = extract_lon_lat(points)
    assert coords == expected_coords, "Extracted coordinates do not match expected"


def test_no_points_generated():
    """Test that no points are generated when num_points is set to 0."""
    test_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    points = generate_random_points(test_polygon, 0)
    assert len(points) == 0, "Points should not be generated"

