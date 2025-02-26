import pytest
from math import pi, tau, sqrt
from fullcontrol.geometry import Point
from fullcontrol.geometry.measure import (
    distance,
    distance_forgiving,
    angleXY_between_3_points,
    path_length
)

def test_distance_3d():
    """Test distance calculation in 3D space"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=1, z=1)
    assert distance(p1, p2) == sqrt(3)  # sqrt(1^2 + 1^2 + 1^2)
    
    p3 = Point(x=3, y=4, z=0)
    assert distance(p1, p3) == 5  # 3-4-5 triangle

def test_distance_2d():
    """Test distance calculation in 2D plane"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=3, y=4, z=0)
    assert distance(p1, p2) == 5  # 3-4-5 triangle
    
    p3 = Point(x=1, y=1, z=0)
    assert abs(distance(p1, p3) - sqrt(2)) < 1e-10

def test_distance_forgiving_missing_coordinates():
    """Test distance calculation with missing coordinates"""
    p1 = Point(x=1, y=None, z=1)
    p2 = Point(x=2, y=None, z=2)
    assert distance_forgiving(p1, p2) == sqrt(2)  # Only x and z contribute
    
    p3 = Point(x=None, y=3, z=None)
    p4 = Point(x=None, y=0, z=None)
    assert distance_forgiving(p3, p4) == 3  # Only y contributes

def test_distance_forgiving_mixed_coordinates():
    """Test distance calculation with mixed present/missing coordinates"""
    p1 = Point(x=1, y=1, z=1)
    p2 = Point(x=2, y=None, z=2)
    assert distance_forgiving(p1, p2) == sqrt(2)  # Only x and z should contribute
    
    p3 = Point(x=0, y=0, z=None)
    p4 = Point(x=3, y=4, z=None)
    assert distance_forgiving(p3, p4) == 5  # 3-4-5 triangle in xy plane

def test_angleXY_right_angle():
    """Test right angle measurement in XY plane"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=0, z=0)
    p3 = Point(x=1, y=1, z=0)
    angle = angleXY_between_3_points(p1, p2, p3)
    assert abs(angle - pi/2) < 1e-10

def test_angleXY_straight_angle():
    """Test straight angle measurement in XY plane"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=0, z=0)
    p3 = Point(x=2, y=0, z=0)
    angle = angleXY_between_3_points(p1, p2, p3)
    assert abs(angle - pi) < 1e-10

def test_angleXY_full_circle():
    """Test full circle angle measurement in XY plane"""
    center = Point(x=0, y=0, z=0)
    p1 = Point(x=1, y=0, z=0)
    points = [
        Point(x=1, y=0, z=0),  # 0 degrees
        Point(x=0, y=1, z=0),  # 90 degrees
        Point(x=-1, y=0, z=0), # 180 degrees
        Point(x=0, y=-1, z=0)  # 270 degrees
    ]
    
    for i in range(len(points)):
        next_i = (i + 1) % len(points)
        angle = angleXY_between_3_points(points[i], center, points[next_i])
        assert abs(angle - pi/2) < 1e-10

def test_angleXY_z_independence():
    """Test that angleXY calculation is independent of z coordinates"""
    p1 = Point(x=1, y=0, z=0)
    p2 = Point(x=0, y=0, z=5)  # Different z coordinate
    p3 = Point(x=0, y=1, z=10)  # Different z coordinate
    angle = angleXY_between_3_points(p1, p2, p3)
    assert abs(angle - pi/2) < 1e-10

def test_path_length_straight():
    """Test path length calculation for straight line segments"""
    points = [
        Point(x=0, y=0, z=0),
        Point(x=3, y=0, z=0),
        Point(x=3, y=4, z=0)
    ]
    assert path_length(points) == 7  # 3 units + 4 units

def test_path_length_square():
    """Test path length calculation for a square path"""
    points = [
        Point(x=0, y=0, z=0),
        Point(x=1, y=0, z=0),
        Point(x=1, y=1, z=0),
        Point(x=0, y=1, z=0),
        Point(x=0, y=0, z=0)  # Back to start
    ]
    assert path_length(points) == 4  # Perimeter of 1x1 square

def test_path_length_3d():
    """Test path length calculation in 3D space"""
    points = [
        Point(x=0, y=0, z=0),
        Point(x=1, y=1, z=1),
        Point(x=2, y=2, z=2)
    ]
    expected_length = 2 * sqrt(3)  # Two segments of length sqrt(3)
    assert abs(path_length(points) - expected_length) < 1e-10

def test_path_length_single_point():
    """Test path length calculation with single point"""
    points = [Point(x=0, y=0, z=0)]
    assert path_length(points) == 0

def test_path_length_two_points():
    """Test path length calculation with two points"""
    points = [
        Point(x=0, y=0, z=0),
        Point(x=1, y=1, z=1)
    ]
    assert abs(path_length(points) - sqrt(3)) < 1e-10