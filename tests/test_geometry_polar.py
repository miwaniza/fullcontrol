import pytest
from math import pi, tau
from fullcontrol.geometry.polar import (
    PolarPoint,
    polar_to_point,
    point_to_polar,
    polar_to_vector,
    _clean_float
)
from fullcontrol.geometry import Point, Vector

def test_polar_point_model():
    """Test PolarPoint model creation and validation"""
    p = PolarPoint(radius=1.0, angle=pi/2)
    assert p.radius == 1.0
    assert p.angle == pi/2

def test_polar_to_point_cardinal_directions():
    """Test polar_to_point conversion at cardinal directions"""
    center = Point(x=0, y=0, z=0)
    # Right (0 degrees)
    p = polar_to_point(center, 1.0, 0)
    assert abs(p.x - 1.0) < 1e-10
    assert abs(p.y) < 1e-10
    # Up (90 degrees)
    p = polar_to_point(center, 1.0, pi/2)
    assert abs(p.x) < 1e-10
    assert abs(p.y - 1.0) < 1e-10
    # Left (180 degrees)
    p = polar_to_point(center, 1.0, pi)
    assert abs(p.x + 1.0) < 1e-10
    assert abs(p.y) < 1e-10
    # Down (270 degrees)
    p = polar_to_point(center, 1.0, 3*pi/2)
    assert abs(p.x) < 1e-10
    assert abs(p.y + 1.0) < 1e-10

def test_polar_to_point_offset_center():
    """Test polar_to_point with non-zero center point"""
    center = Point(x=1, y=2, z=3)
    p = polar_to_point(center, 1.0, 0)
    assert abs(p.x - 2.0) < 1e-10  # center.x + radius
    assert abs(p.y - 2.0) < 1e-10  # center.y
    assert p.z == center.z

def test_point_to_polar_quadrants():
    """Test point_to_polar conversion in all quadrants"""
    origin = Point(x=0, y=0, z=0)
    
    # First quadrant
    target = Point(x=1, y=1, z=0)
    polar = point_to_polar(target, origin)
    assert abs(polar.radius - 2**0.5) < 1e-10
    assert abs(polar.angle - pi/4) < 1e-10
    
    # Second quadrant
    target = Point(x=-1, y=1, z=0)
    polar = point_to_polar(target, origin)
    assert abs(polar.radius - 2**0.5) < 1e-10
    assert abs(polar.angle - 3*pi/4) < 1e-10
    
    # Third quadrant
    target = Point(x=-1, y=-1, z=0)
    polar = point_to_polar(target, origin)
    assert abs(polar.radius - 2**0.5) < 1e-10
    assert abs(polar.angle - 5*pi/4) < 1e-10
    
    # Fourth quadrant
    target = Point(x=1, y=-1, z=0)
    polar = point_to_polar(target, origin)
    assert abs(polar.radius - 2**0.5) < 1e-10
    assert abs(polar.angle - 7*pi/4) < 1e-10

def test_point_to_polar_offset_origin():
    """Test point_to_polar with non-zero origin point"""
    origin = Point(x=1, y=1, z=0)
    target = Point(x=2, y=2, z=0)
    polar = point_to_polar(target, origin)
    assert abs(polar.radius - 2**0.5) < 1e-10
    assert abs(polar.angle - pi/4) < 1e-10

def test_polar_to_vector():
    """Test polar_to_vector conversion"""
    # Unit vectors in cardinal directions
    v = polar_to_vector(1.0, 0)
    assert abs(v.x - 1.0) < 1e-10
    assert abs(v.y) < 1e-10
    
    v = polar_to_vector(1.0, pi/2)
    assert abs(v.x) < 1e-10
    assert abs(v.y - 1.0) < 1e-10
    
    # 45-degree vector with length 2
    v = polar_to_vector(2.0, pi/4)
    assert abs(v.x - 2**0.5) < 1e-10
    assert abs(v.y - 2**0.5) < 1e-10

def test_numerical_stability():
    """Test numerical stability near zero"""
    # Test points very close to axes
    p = polar_to_point(Point(x=0, y=0, z=0), 1.0, 1e-11)
    assert p.y == 0.0  # Should be cleaned to exactly zero
    
    # Test very small radius
    p = polar_to_point(Point(x=0, y=0, z=0), 1e-11, 0)
    assert p.x == 0.0
    assert p.y == 0.0

def test_full_circle_roundtrip():
    """Test converting points around a full circle and back"""
    origin = Point(x=0, y=0, z=0)
    angles = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4]
    
    for angle in angles:
        # Convert to cartesian
        p1 = polar_to_point(origin, 1.0, angle)
        # Convert back to polar
        polar = point_to_polar(p1, origin)
        # Convert back to cartesian
        p2 = polar_to_point(origin, polar.radius, polar.angle)
        
        # Check that the points match
        assert abs(p1.x - p2.x) < 1e-10
        assert abs(p1.y - p2.y) < 1e-10
        assert p1.z == p2.z