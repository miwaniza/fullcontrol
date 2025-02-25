import pytest
from math import pi, tau, sin
from fullcontrol.geometry import Point, Vector
from fullcontrol.geometry.waves import (
    squarewaveXY, squarewaveXYpolar, trianglewaveXYpolar, sinewaveXYpolar
)

def test_squarewave_vector():
    """Test square wave generation using vector direction"""
    start = Point(x=0, y=0, z=0)
    direction = Vector(x=1, y=0)  # Horizontal wave
    points = squarewaveXY(start, direction, amplitude=2, line_spacing=2, periods=2)
    
    # Should have 9 points for 2 periods: start + (up, right, down, right) * 2
    assert len(points) == 9
    # Check first period
    assert points[0].x == 0 and points[0].y == 0  # Start
    assert points[1].x == 0 and points[1].y == 2  # Up
    assert points[2].x == 1 and points[2].y == 2  # Right
    assert points[3].x == 1 and points[3].y == 0  # Down
    assert points[4].x == 2 and points[4].y == 0  # Right

def test_squarewave_polar():
    """Test square wave generation using polar direction"""
    start = Point(x=0, y=0, z=0)
    points = squarewaveXYpolar(
        start,
        direction_polar=0,  # Horizontal wave
        amplitude=2,
        line_spacing=2,
        periods=1,
        extra_half_period=True
    )
    
    # Should have 6 points for 1 period + half: start + (up, right, down, right) + up
    assert len(points) == 6
    assert points[0].x == 0 and points[0].y == 0  # Start
    assert abs(points[-1].y - 2) < 1e-10  # Ends at top

def test_trianglewave_basic():
    """Test basic triangle wave generation"""
    start = Point(x=0, y=0, z=0)
    points = trianglewaveXYpolar(
        start,
        direction_polar=0,  # Horizontal wave
        amplitude=1,
        tip_separation=2,
        periods=1
    )
    
    # Check number of points and basic shape
    assert len(points) == 4  # start + top tip + bottom tip + end position
    assert abs(points[1].y - 1) < 1e-10  # Top tip
    assert abs(points[2].y + 1) < 1e-10  # Bottom tip

def test_sinewave_basic():
    """Test basic sine wave generation"""
    start = Point(x=0, y=0, z=0)
    points = sinewaveXYpolar(
        start,
        direction_polar=0,
        amplitude=1,
        period_length=tau,
        periods=1,
        segments_per_period=4  # Low number for easy testing
    )
    
    # Should have 5 points for 1 period with 4 segments (including start and end)
    assert len(points) == 5
    # Check key points match sine wave shape
    assert abs(points[0].y) < 1e-10  # Start at y=0
    assert abs(points[2].y - 1) < 1e-10  # Peak at y=1
    assert abs(points[4].y) < 1e-10  # End at y=0

def test_sinewave_phase_shift():
    """Test sine wave with phase shift"""
    start = Point(x=0, y=0, z=0)
    points = sinewaveXYpolar(
        start,
        direction_polar=0,
        amplitude=1,
        period_length=tau,
        periods=1,
        segments_per_period=4,
        phase_shift=pi/2  # Quarter period phase shift
    )
    
    # First point should start at maximum (y=1) due to pi/2 phase shift
    assert abs(points[0].y - 1) < 1e-10
    # Midpoint should be at y=0
    assert abs(points[2].y) < 1e-10
    # End point should be at minimum (y=-1)
    assert abs(points[-1].y + 1) < 1e-10

def test_wave_direction():
    """Test wave generation in different directions"""
    start = Point(x=0, y=0, z=0)
    # Test vertical wave (90 degrees)
    points = squarewaveXYpolar(
        start,
        direction_polar=pi/2,
        amplitude=1,
        line_spacing=1,
        periods=1
    )
    
    # First movement should be in -x direction (perpendicular to vertical)
    assert abs(points[1].x + 1) < 1e-10
    assert abs(points[1].y) < 1e-10

def test_wave_z_preservation():
    """Test that waves preserve z-coordinate"""
    start = Point(x=0, y=0, z=5)
    
    # Test z preservation for all wave types
    square = squarewaveXYpolar(start, 0, 1, 1, 1)
    triangle = trianglewaveXYpolar(start, 0, 1, 1, 1)
    sine = sinewaveXYpolar(start, 0, 1, tau, 1)
    
    assert all(p.z == 5 for p in square)
    assert all(p.z == 5 for p in triangle)
    assert all(p.z == 5 for p in sine)