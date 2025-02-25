import pytest
from math import pi, cos, sin, sqrt
from fullcontrol.geometry import Point
from lab.fullcontrol.geometry.rotate import (
    dot_product, cross_product, rotate, rotate_geometry, rotate_copy_geometry
)

def test_dot_product():
    """Test dot product helper function"""
    v1 = Point(x=1, y=0, z=0)
    v2 = Point(x=0, y=1, z=0)
    assert dot_product(v1, v2) == 0  # Perpendicular vectors
    
    v1 = Point(x=1, y=2, z=3)
    v2 = Point(x=4, y=5, z=6)
    assert dot_product(v1, v2) == 32  # 1*4 + 2*5 + 3*6
    
    # Test with None values
    v1 = Point(x=1, y=None, z=3)
    v2 = Point(x=4, y=5, z=6)
    assert dot_product(v1, v2) == 22  # 1*4 + 3*6

def test_cross_product():
    """Test cross product helper function"""
    # Unit vectors
    v1 = Point(x=1, y=0, z=0)
    v2 = Point(x=0, y=1, z=0)
    result = cross_product(v1, v2)
    assert result.x == 0
    assert result.y == 0
    assert result.z == 1
    
    # Test with None values
    v1 = Point(x=1, y=None, z=0)
    v2 = Point(x=0, y=1, z=0)
    result = cross_product(v1, v2)
    assert result.x == 0
    assert result.y == 0
    assert result.z == 1

def test_rotate_point_about_z():
    """Test rotating a point about the Z axis"""
    # Point on X axis, rotate 90 degrees about Z
    p = Point(x=1, y=0, z=0)
    origin = Point(x=0, y=0, z=0)
    z_axis = Point(x=0, y=0, z=1)
    
    rotated = rotate_geometry(p, origin, z_axis, pi/2)
    assert abs(rotated.x) < 1e-10
    assert abs(rotated.y - 1) < 1e-10
    assert abs(rotated.z) < 1e-10

def test_rotate_point_about_arbitrary_axis():
    """Test rotating a point about an arbitrary axis"""
    # Point and arbitrary axis
    p = Point(x=1, y=0, z=0)
    axis_start = Point(x=0, y=0, z=0)
    axis_end = Point(x=1, y=1, z=1)  # 45 degree diagonal
    
    # Full rotation should return to start (approximately)
    rotated = rotate_geometry(p, axis_start, axis_end, 2*pi)
    assert abs(rotated.x - p.x) < 1e-10
    assert abs(rotated.y - p.y) < 1e-10
    assert abs(rotated.z - p.z) < 1e-10

def test_rotate_with_offset_axis():
    """Test rotating around an axis that doesn't pass through origin"""
    p = Point(x=0, y=0, z=0)
    axis_start = Point(x=1, y=0, z=0)
    axis_end = Point(x=1, y=0, z=1)
    
    # 180 degree rotation should move point to opposite side of axis
    rotated = rotate_geometry(p, axis_start, axis_end, pi)
    assert abs(rotated.x - 2) < 1e-10
    assert abs(rotated.y) < 1e-10
    assert abs(rotated.z) < 1e-10

def test_rotate_list_of_points():
    """Test rotating multiple points"""
    points = [
        Point(x=1, y=0, z=0),
        Point(x=1, y=1, z=0),
        Point(x=0, y=1, z=0)
    ]
    origin = Point(x=0, y=0, z=0)
    z_axis = Point(x=0, y=0, z=1)
    
    # Rotate 90 degrees about Z axis
    rotated = rotate_geometry(points, origin, z_axis, pi/2)
    
    # First point should go from (1,0,0) to (0,1,0)
    assert abs(rotated[0].x) < 1e-10
    assert abs(rotated[0].y - 1) < 1e-10
    assert abs(rotated[0].z) < 1e-10
    
    # Second point should go from (1,1,0) to (-1,1,0)
    assert abs(rotated[1].x + 1) < 1e-10
    assert abs(rotated[1].y - 1) < 1e-10
    assert abs(rotated[1].z) < 1e-10

def test_rotate_with_direction_string():
    """Test rotation using direction string ('x', 'y', or 'z')"""
    p = Point(x=1, y=0, z=0)
    origin = Point(x=0, y=0, z=0)
    
    # Rotate 90 degrees about Y axis using string direction
    rotated = rotate(p, origin, 'y', pi/2)
    assert abs(rotated.x) < 1e-10
    assert abs(rotated.y) < 1e-10
    assert abs(rotated.z + 1) < 1e-10

def test_rotate_copy():
    """Test creating multiple rotated copies"""
    p = Point(x=1, y=0, z=0)
    origin = Point(x=0, y=0, z=0)
    
    # Create 4 copies 90 degrees apart about Z axis
    copies = rotate(p, origin, 'z', pi/2, copy=True, copy_quantity=4)
    
    assert len(copies) == 4
    # Original point (1,0,0)
    assert abs(copies[0].x - 1) < 1e-10
    assert abs(copies[0].y) < 1e-10
    # 90 degrees (0,1,0)
    assert abs(copies[1].x) < 1e-10
    assert abs(copies[1].y - 1) < 1e-10
    # 180 degrees (-1,0,0)
    assert abs(copies[2].x + 1) < 1e-10
    assert abs(copies[2].y) < 1e-10
    # 270 degrees (0,-1,0)
    assert abs(copies[3].x) < 1e-10
    assert abs(copies[3].y + 1) < 1e-10

def test_rotate_non_point_elements():
    """Test that non-Point elements in lists pass through unchanged"""
    mixed_list = [
        Point(x=1, y=0, z=0),
        "some string",
        Point(x=0, y=1, z=0),
        42
    ]
    origin = Point(x=0, y=0, z=0)
    z_axis = Point(x=0, y=0, z=1)
    
    rotated = rotate_geometry(mixed_list, origin, z_axis, pi/2)
    
    assert len(rotated) == 4
    assert isinstance(rotated[0], Point)
    assert rotated[1] == "some string"
    assert isinstance(rotated[2], Point)
    assert rotated[3] == 42