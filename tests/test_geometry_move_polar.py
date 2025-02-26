import pytest
import math
from fullcontrol.geometry.move_polar import move_polar, move_geometry_polar, copy_geometry_polar
from fullcontrol.point import Point


def test_move_polar_point():
    """Test move_polar function with a Point object"""
    center = Point(x=0, y=0, z=0)
    point = Point(x=10, y=0, z=5)
    
    # Move 90 degrees (pi/2 radians) counterclockwise and increase radius by 5
    result = move_polar(point, center, 5, math.pi/2)
    
    # Should now be at (0, 15, 5) - on y-axis with radius 15
    assert math.isclose(result.x, 0, abs_tol=1e-10)
    assert math.isclose(result.y, 15)
    assert result.z == 5  # z should remain unchanged
    
    # Original point should not be modified
    assert point.x == 10
    assert point.y == 0
    assert point.z == 5


def test_move_polar_list():
    """Test move_polar function with a list of Points and other objects"""
    center = Point(x=0, y=0, z=0)
    points = [
        Point(x=10, y=0, z=5),
        "not a point",
        Point(x=0, y=10, z=5)
    ]
    
    # Rotate 90 degrees and keep same radius
    result = move_polar(points, center, 0, math.pi/2)
    
    assert len(result) == 3
    # First point - rotated 90 degrees
    assert math.isclose(result[0].x, 0, abs_tol=1e-10)
    assert math.isclose(result[0].y, 10)
    assert result[0].z == 5
    
    # Non-Point element should pass through
    assert result[1] == "not a point"
    
    # Second point - rotated 90 degrees
    assert math.isclose(result[2].x, -10, abs_tol=1e-10)
    assert math.isclose(result[2].y, 0, abs_tol=1e-10)
    assert result[2].z == 5
    
    # Original list should not be modified
    assert points[0].x == 10
    assert points[0].y == 0


def test_move_polar_with_copy():
    """Test move_polar with copy option"""
    center = Point(x=0, y=0, z=0)
    point = Point(x=10, y=0, z=5)
    
    # Create 3 copies, each rotated by 90 degrees from the previous
    result = move_polar(point, center, 0, math.pi/2, copy=True, copy_quantity=4)
    
    assert len(result) == 4
    
    # First copy (i=0) - original position
    assert math.isclose(result[0].x, 10)
    assert math.isclose(result[0].y, 0)
    
    # Second copy (i=1) - rotated 90 degrees
    assert math.isclose(result[1].x, 0, abs_tol=1e-10)
    assert math.isclose(result[1].y, 10)
    
    # Third copy (i=2) - rotated 180 degrees
    assert math.isclose(result[2].x, -10)
    assert math.isclose(result[2].y, 0, abs_tol=1e-10)
    
    # Fourth copy (i=3) - rotated 270 degrees
    assert math.isclose(result[3].x, 0, abs_tol=1e-10)
    assert math.isclose(result[3].y, -10)


def test_move_polar_with_changing_radius():
    """Test move_polar with changing radius"""
    center = Point(x=0, y=0, z=0)
    point = Point(x=10, y=0, z=5)
    
    # Move point outward by 5 units without rotation
    result = move_polar(point, center, 5, 0)
    
    assert math.isclose(result.x, 15)
    assert math.isclose(result.y, 0)
    assert result.z == 5


def test_copy_geometry_polar_changes_both_radius_and_angle():
    """Test copy_geometry_polar with changes to both radius and angle"""
    center = Point(x=0, y=0, z=0)
    point = Point(x=10, y=0, z=5)
    
    # Create 3 copies, increasing radius by 5 and rotating by 45 degrees each time
    result = copy_geometry_polar(point, center, 5, math.pi/4, 3)
    
    assert len(result) == 3
    
    # First copy (i=0) - original position
    assert math.isclose(result[0].x, 10)
    assert math.isclose(result[0].y, 0)
    
    # Second copy (i=1) - radius=15, angle=45 degrees
    assert math.isclose(result[1].x, 15 * math.cos(math.pi/4))
    assert math.isclose(result[1].y, 15 * math.sin(math.pi/4))
    
    # Third copy (i=2) - radius=20, angle=90 degrees
    assert math.isclose(result[2].x, 0, abs_tol=1e-10)
    assert math.isclose(result[2].y, 20)