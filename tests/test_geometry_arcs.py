import pytest
from math import pi, tau
from fullcontrol.geometry.arcs import arcXY, variable_arcXY, elliptical_arcXY, _clean_float
from fullcontrol.geometry import Point

def test_clean_float():
    """Test the floating point cleanup function"""
    assert _clean_float(1e-11) == 0.0
    assert _clean_float(1e-9) == 1e-9
    assert _clean_float(-1e-11) == 0.0
    assert _clean_float(1.0) == 1.0

def test_arcXY_full_circle():
    """Test creating a full circle using arcXY"""
    center = Point(x=0, y=0, z=0)
    points = arcXY(center, radius=1.0, start_angle=0, arc_angle=tau, segments=4)
    assert len(points) == 5  # 4 segments + 1 closing point
    assert abs(points[0].x - 1.0) < 1e-10  # First point should be at (1,0)
    assert abs(points[0].y) < 1e-10
    # Last point should match first point for full circle
    assert abs(points[-1].x - points[0].x) < 1e-10
    assert abs(points[-1].y - points[0].y) < 1e-10

def test_arcXY_quarter_circle():
    """Test creating a quarter circle using arcXY"""
    center = Point(x=1, y=1, z=1)
    points = arcXY(center, radius=2.0, start_angle=0, arc_angle=pi/2, segments=2)
    assert len(points) == 3
    # First point should be at (radius,0) relative to center
    assert abs(points[0].x - 3.0) < 1e-10
    assert abs(points[0].y - 1.0) < 1e-10
    # Last point should be at (0,radius) relative to center
    assert abs(points[-1].x - 1.0) < 1e-10
    assert abs(points[-1].y - 3.0) < 1e-10
    # Z coordinate should remain constant
    assert all(p.z == center.z for p in points)

def test_variable_arcXY_radius_change():
    """Test creating an arc with varying radius"""
    center = Point(x=0, y=0, z=0)
    points = variable_arcXY(
        center, 
        start_radius=1.0,
        start_angle=0,
        arc_angle=pi/2,
        segments=2,
        radius_change=1.0
    )
    assert len(points) == 3
    # Check start and end radii
    start_radius = (points[0].x**2 + points[0].y**2)**0.5
    end_radius = (points[-1].x**2 + points[-1].y**2)**0.5
    assert abs(start_radius - 1.0) < 1e-10
    assert abs(end_radius - 2.0) < 1e-10

def test_variable_arcXY_z_change():
    """Test creating an arc with varying z height"""
    center = Point(x=0, y=0, z=1)
    points = variable_arcXY(
        center,
        start_radius=1.0,
        start_angle=0,
        arc_angle=pi,
        segments=2,
        z_change=2.0
    )
    assert len(points) == 3
    assert abs(points[0].z - 1.0) < 1e-10
    assert abs(points[-1].z - 3.0) < 1e-10

def test_elliptical_arcXY_aspect_ratio():
    """Test creating elliptical arcs with different aspect ratios"""
    center = Point(x=0, y=0, z=0)
    points = elliptical_arcXY(
        center,
        a=2.0,  # x radius
        b=1.0,  # y radius
        start_angle=0,
        arc_angle=pi/2,
        segments=2
    )
    assert len(points) == 3
    # Check first point (should be at (a,0))
    assert abs(points[0].x - 2.0) < 1e-10
    assert abs(points[0].y) < 1e-10
    # Check last point (should be at (0,b))
    assert abs(points[-1].x) < 1e-10
    assert abs(points[-1].y - 1.0) < 1e-10

def test_elliptical_arcXY_offset_center():
    """Test creating elliptical arcs with offset center point"""
    center = Point(x=1, y=2, z=3)
    points = elliptical_arcXY(
        center,
        a=1.0,
        b=1.0,
        start_angle=0,
        arc_angle=pi/2,
        segments=2
    )
    # First point should be offset from center by (a,0)
    assert abs(points[0].x - 2.0) < 1e-10  # center.x + a
    assert abs(points[0].y - 2.0) < 1e-10  # center.y
    # Last point should be offset from center by (0,b)
    assert abs(points[-1].x - 1.0) < 1e-10  # center.x
    assert abs(points[-1].y - 3.0) < 1e-10  # center.y + b
    # Z coordinate should remain constant
    assert all(p.z == center.z for p in points)