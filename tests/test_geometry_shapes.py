import pytest
from math import pi, tau, atan2, sqrt
from fullcontrol.geometry import Point
from fullcontrol.geometry.shapes import (
    rectangleXY,
    circleXY,
    circleXY_3pt,
    ellipseXY,
    polygonXY,
    spiralXY,
    helixZ
)

def test_rectangleXY_basic():
    """Test basic rectangle generation"""
    start = Point(x=0, y=0, z=0)
    points = rectangleXY(start, x_size=2, y_size=3)
    
    assert len(points) == 5  # Should have 5 points (including start/end)
    assert points[0].x == 0 and points[0].y == 0  # Start point
    assert points[1].x == 0 and points[1].y == 3  # Left side
    assert points[2].x == 2 and points[2].y == 3  # Top side
    assert points[3].x == 2 and points[3].y == 0  # Right side
    assert points[4].x == 0 and points[4].y == 0  # Back to start

def test_rectangleXY_clockwise():
    """Test clockwise rectangle generation"""
    start = Point(x=1, y=1, z=1)
    points = rectangleXY(start, x_size=2, y_size=2, cw=True)
    
    assert len(points) == 5
    assert points[1].x == 3 and points[1].y == 1  # First move right
    assert points[2].x == 3 and points[2].y == 3  # Up
    assert points[3].x == 1 and points[3].y == 3  # Left
    assert points[4].x == 1 and points[4].y == 1  # Down to start

def test_circleXY_basic():
    """Test basic circle generation"""
    center = Point(x=0, y=0, z=0)
    points = circleXY(center, radius=1, start_angle=0, segments=4)
    
    assert len(points) == 5  # 4 segments + closing point
    # Check cardinal points
    assert abs(points[0].x - 1) < 1e-10 and abs(points[0].y) < 1e-10  # Right
    assert abs(points[1].x) < 1e-10 and abs(points[1].y - 1) < 1e-10  # Top
    assert abs(points[2].x + 1) < 1e-10 and abs(points[2].y) < 1e-10  # Left
    assert abs(points[3].x) < 1e-10 and abs(points[3].y + 1) < 1e-10  # Bottom

def test_circleXY_3pt_basic():
    """Test circle generation through three points"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=0, z=0)
    p3 = Point(x=0, y=1, z=0)
    points = circleXY_3pt(p1, p2, p3, start_angle=0, segments=4)
    
    # Should form a circle with radius = 1/√2 centered at (0.5, 0.5)
    radius = (2**0.5) / 2
    assert len(points) == 5
    for p in points[:-1]:  # Exclude last point which is same as first
        # Check if point is approximately radius distance from center
        dist_from_center = ((p.x - 0.5)**2 + (p.y - 0.5)**2)**0.5
        assert abs(dist_from_center - radius) < 1e-10

def test_ellipseXY_basic():
    """Test basic ellipse generation"""
    center = Point(x=0, y=0, z=0)
    points = ellipseXY(center, a=2, b=1, start_angle=0, segments=4)
    
    assert len(points) == 5
    # Check points at 0, 90, 180, 270 degrees
    assert abs(points[0].x - 2) < 1e-10 and abs(points[0].y) < 1e-10  # Right
    assert abs(points[1].x) < 1e-10 and abs(points[1].y - 1) < 1e-10  # Top
    assert abs(points[2].x + 2) < 1e-10 and abs(points[2].y) < 1e-10  # Left
    assert abs(points[3].x) < 1e-10 and abs(points[3].y + 1) < 1e-10  # Bottom

def test_polygonXY_triangle():
    """Test polygon generation with 3 sides (triangle)"""
    center = Point(x=0, y=0, z=0)
    points = polygonXY(center, enclosing_radius=1, start_angle=0, sides=3)
    
    assert len(points) == 4  # 3 vertices + closing point
    # Vertices should be equally spaced around circle
    angles = []
    for i in range(3):
        angle = atan2(points[i].y, points[i].x)
        if angle < 0:
            angle += tau  # Normalize to [0, tau)
        angles.append(angle)
    
    # Check angles are approximately 120 degrees apart
    for i in range(3):
        next_i = (i + 1) % 3
        angle_diff = abs(angles[next_i] - angles[i])
        if angle_diff > pi:
            angle_diff = tau - angle_diff
        assert abs(angle_diff - tau/3) < 1e-10

def test_spiralXY_basic():
    """Test basic spiral generation"""
    center = Point(x=0, y=0, z=0)
    points = spiralXY(
        center,
        start_radius=1,
        end_radius=2,
        start_angle=0,
        n_turns=1,
        segments=4
    )
    
    assert len(points) == 5
    # Check first and last points
    assert abs(points[0].x - 1) < 1e-10  # Start at radius 1
    final_radius = sqrt(points[-1].x**2 + points[-1].y**2)
    assert abs(final_radius - 2) < 1e-10  # End at radius 2

def test_helixZ_basic():
    """Test basic helix generation"""
    center = Point(x=0, y=0, z=0)
    points = helixZ(
        center,
        start_radius=1,
        end_radius=1,  # Constant radius
        start_angle=0,
        n_turns=1,
        pitch_z=2,  # Rise of 2 units per turn
        segments=4
    )
    
    assert len(points) == 5
    # Check start and end points
    assert abs(points[0].x - 1) < 1e-10 and abs(points[0].y) < 1e-10 and abs(points[0].z) < 1e-10
    assert abs(points[-1].x - 1) < 1e-10 and abs(points[-1].y) < 1e-10 and abs(points[-1].z - 2) < 1e-10

def test_shape_z_preservation():
    """Test that shapes preserve z-coordinate of center/start point"""
    z = 5
    start = Point(x=0, y=0, z=z)
    center = Point(x=0, y=0, z=z)
    
    # Test all 2D shapes
    rect_points = rectangleXY(start, 1, 1)
    assert all(p.z == z for p in rect_points)
    
    circle_points = circleXY(center, 1, 0)
    assert all(p.z == z for p in circle_points)
    
    ellipse_points = ellipseXY(center, 2, 1, 0)
    assert all(p.z == z for p in ellipse_points)
    
    polygon_points = polygonXY(center, 1, 0, 6)
    assert all(p.z == z for p in polygon_points)
    
    spiral_points = spiralXY(center, 1, 2, 0, 1, 4)
    assert all(p.z == z for p in spiral_points)

def test_clockwise_direction():
    """Test clockwise generation of shapes"""
    center = Point(x=0, y=0, z=0)
    
    # Test circle clockwise vs counter-clockwise
    ccw_points = circleXY(center, 1, 0, segments=4)
    cw_points = circleXY(center, 1, 0, segments=4, cw=True)
    
    # Y coordinates should be opposite
    assert abs(ccw_points[1].y + cw_points[1].y) < 1e-10
    assert abs(ccw_points[3].y + cw_points[3].y) < 1e-10