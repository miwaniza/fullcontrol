import pytest
from fullcontrol.geometry import Point
from fullcontrol.geometry.midpoint import midpoint, interpolated_point

def test_midpoint_basic():
    """Test basic midpoint calculation"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=2, y=4, z=6)
    mid = midpoint(p1, p2)
    
    assert mid.x == 1
    assert mid.y == 2
    assert mid.z == 3

def test_midpoint_negative_coords():
    """Test midpoint calculation with negative coordinates"""
    p1 = Point(x=-2, y=-4, z=-6)
    p2 = Point(x=2, y=4, z=6)
    mid = midpoint(p1, p2)
    
    assert mid.x == 0
    assert mid.y == 0
    assert mid.z == 0

def test_midpoint_with_none():
    """Test midpoint calculation with None coordinates"""
    p1 = Point(x=0, y=None, z=0)
    p2 = Point(x=2, y=None, z=2)
    mid = midpoint(p1, p2)
    
    assert mid.x == 1
    assert mid.y is None
    assert mid.z == 1

def test_interpolated_point_basic():
    """Test basic interpolated point calculation"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=10, y=10, z=10)
    
    # Test 25% interpolation
    p_25 = interpolated_point(p1, p2, 0.25)
    assert p_25.x == 2.5
    assert p_25.y == 2.5
    assert p_25.z == 2.5
    
    # Test 75% interpolation
    p_75 = interpolated_point(p1, p2, 0.75)
    assert p_75.x == 7.5
    assert p_75.y == 7.5
    assert p_75.z == 7.5

def test_interpolated_point_start_end():
    """Test interpolated point at start and end points"""
    p1 = Point(x=1, y=1, z=1)
    p2 = Point(x=2, y=2, z=2)
    
    # Should match start point
    p_start = interpolated_point(p1, p2, 0.0)
    assert p_start.x == p1.x
    assert p_start.y == p1.y
    assert p_start.z == p1.z
    
    # Should match end point
    p_end = interpolated_point(p1, p2, 1.0)
    assert p_end.x == p2.x
    assert p_end.y == p2.y
    assert p_end.z == p2.z

def test_interpolated_point_negative_coords():
    """Test interpolated point with negative coordinates"""
    p1 = Point(x=-2, y=-2, z=-2)
    p2 = Point(x=2, y=2, z=2)
    p_mid = interpolated_point(p1, p2, 0.5)
    
    assert p_mid.x == 0
    assert p_mid.y == 0
    assert p_mid.z == 0

def test_interpolated_point_with_none():
    """Test interpolated point calculation with None coordinates"""
    p1 = Point(x=0, y=None, z=0)
    p2 = Point(x=10, y=None, z=10)
    p_inter = interpolated_point(p1, p2, 0.3)
    
    assert p_inter.x == 3
    assert p_inter.y is None
    assert p_inter.z == 3

def test_interpolated_point_mixed_none():
    """Test interpolated point with mixed None/value coordinates"""
    p1 = Point(x=0, y=0, z=None)
    p2 = Point(x=10, y=None, z=10)
    p_inter = interpolated_point(p1, p2, 0.5)
    
    assert p_inter.x == 5
    assert p_inter.y is None
    assert p_inter.z == 5

def test_interpolated_point_extrapolation():
    """Test interpolated point with extrapolation (fraction > 1 or < 0)"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=1, z=1)
    
    # Test extrapolation beyond p2
    p_beyond = interpolated_point(p1, p2, 2.0)
    assert p_beyond.x == 2
    assert p_beyond.y == 2
    assert p_beyond.z == 2
    
    # Test extrapolation before p1
    p_before = interpolated_point(p1, p2, -1.0)
    assert p_before.x == -1
    assert p_before.y == -1
    assert p_before.z == -1