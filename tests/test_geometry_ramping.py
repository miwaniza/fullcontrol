import pytest
import math
from fullcontrol.geometry.ramping import ramp_xyz, ramp_polar
from fullcontrol.point import Point
from fullcontrol.geometry import Vector


def test_ramp_xyz():
    """Test ramp_xyz function to linearly adjust x, y, z values"""
    points = [
        Point(x=10, y=20, z=30),
        Point(x=10, y=20, z=30),
        Point(x=10, y=20, z=30),
    ]
    
    result = ramp_xyz(points, x_change=10, y_change=20, z_change=30)
    
    # Check if result is the same object (ramp_xyz returns the modified list)
    assert result is points
    
    # First element should be a Point
    assert isinstance(points[0], Point)
    # Check first point (should be unchanged or have minimal change)
    assert math.isclose(points[0].x, 10)
    assert math.isclose(points[0].y, 20)
    assert math.isclose(points[0].z, 30)
    
    # Second element should be a Point
    assert isinstance(points[1], Point)
    # Check middle point
    assert math.isclose(points[1].x, 15)
    assert math.isclose(points[1].y, 30)
    assert math.isclose(points[1].z, 45)
    
    # Third element should be a Point
    assert isinstance(points[2], Point)
    # Check last point (should have the full change added)
    assert math.isclose(points[2].x, 20)
    assert math.isclose(points[2].y, 40)
    assert math.isclose(points[2].z, 60)


def test_ramp_xyz_partial_changes():
    """Test ramp_xyz with changes to only some dimensions"""
    points = [
        Point(x=10, y=20, z=30),
        Point(x=10, y=20, z=30),
        Point(x=10, y=20, z=30),
    ]
    
    result = ramp_xyz(points, z_change=30)
    
    # First element should be a Point
    assert isinstance(points[0], Point)
    # Check first point
    assert math.isclose(points[0].x, 10)
    assert math.isclose(points[0].y, 20)
    assert math.isclose(points[0].z, 30)
    
    # Second element should be a Point
    assert isinstance(points[1], Point)
    # Check middle point
    assert math.isclose(points[1].x, 10)
    assert math.isclose(points[1].y, 20)
    assert math.isclose(points[1].z, 45)
    
    # Third element should be a Point
    assert isinstance(points[2], Point)
    # Check last point
    assert math.isclose(points[2].x, 10)
    assert math.isclose(points[2].y, 20)
    assert math.isclose(points[2].z, 60)


def test_ramp_polar():
    """Test ramp_polar function to linearly adjust radius and angle"""
    center = Point(x=0, y=0, z=0)
    
    # Create 3 points at radius=10, angle=0 (on x-axis)
    points = [
        Point(x=10, y=0, z=0),
        Point(x=10, y=0, z=0),
        Point(x=10, y=0, z=0),
    ]
    
    # Ramp radius by +10 and angle by +math.pi/2 (90 degrees)
    result = ramp_polar(points, center, radius_change=10, angle_change=math.pi/2)
    
    # Check if result is the same object (ramp_polar returns the modified list)
    assert result is points
    
    # First element should be a Point
    assert isinstance(points[0], Point)
    # Check first point (should be unchanged or have minimal change)
    assert math.isclose(points[0].x, 10)
    assert math.isclose(points[0].y, 0)
    
    # Second element should be a Point
    assert isinstance(points[1], Point)
    # Check middle point - should be at radius=15, angle=pi/4 (45 degrees)
    expected_x = 15 * math.cos(math.pi/4)
    expected_y = 15 * math.sin(math.pi/4)
    assert math.isclose(points[1].x, expected_x)
    assert math.isclose(points[1].y, expected_y)
    
    # Third element should be a Point
    assert isinstance(points[2], Point)
    # Check last point - should be at radius=20, angle=pi/2 (90 degrees)
    assert math.isclose(points[2].x, 0, abs_tol=1e-10)
    assert math.isclose(points[2].y, 20)


def test_ramp_polar_radius_only():
    """Test ramp_polar with only radius change"""
    center = Point(x=0, y=0, z=0)
    
    # Create 3 points at radius=10, angle=0 (on x-axis)
    points = [
        Point(x=10, y=0, z=0),
        Point(x=10, y=0, z=0),
        Point(x=10, y=0, z=0),
    ]
    
    # Ramp radius by +10
    result = ramp_polar(points, center, radius_change=10)
    
    # Check first point
    assert math.isclose(points[0].x, 10)
    assert math.isclose(points[0].y, 0)
    
    # Check middle point
    assert math.isclose(points[1].x, 15)
    assert math.isclose(points[1].y, 0)
    
    # Check last point
    assert math.isclose(points[2].x, 20)
    assert math.isclose(points[2].y, 0)