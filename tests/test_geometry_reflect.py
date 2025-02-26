import pytest
from math import pi, tau
from fullcontrol.geometry import Point
from fullcontrol.geometry.reflect import reflectXY, reflectXY_mc
from fullcontrol.geometry.reflect_polar import reflectXYpolar

def test_reflectXY_horizontal():
    """Test reflection about a horizontal line (x-axis)"""
    point = Point(x=2, y=3, z=1)
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=0, z=0)
    
    reflected = reflectXY(point, p1, p2)
    assert reflected.x == 2
    assert reflected.y == -3
    assert reflected.z == 1  # z-coordinate should remain unchanged

def test_reflectXY_vertical():
    """Test reflection about a vertical line (y-axis)"""
    point = Point(x=2, y=3, z=1)
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=0, y=1, z=0)
    
    reflected = reflectXY(point, p1, p2)
    assert reflected.x == -2
    assert reflected.y == 3
    assert reflected.z == 1

def test_reflectXY_diagonal():
    """Test reflection about a 45-degree diagonal line"""
    point = Point(x=1, y=0, z=1)
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=1, z=0)
    
    reflected = reflectXY(point, p1, p2)
    assert abs(reflected.x - 0) < 1e-10
    assert abs(reflected.y - 1) < 1e-10
    assert reflected.z == 1

def test_reflectXY_mc_horizontal():
    """Test reflection about y=c line using slope-intercept form"""
    point = Point(x=2, y=3, z=1)
    
    # Reflect about y=0 (x-axis)
    reflected = reflectXY_mc(point, m_reflect=0, c_reflect=0)
    assert reflected.x == 2
    assert reflected.y == -3
    assert reflected.z == 1

def test_reflectXY_mc_diagonal():
    """Test reflection about y=x line using slope-intercept form"""
    point = Point(x=1, y=0, z=1)
    
    # Reflect about y=x (45-degree line through origin)
    reflected = reflectXY_mc(point, m_reflect=1, c_reflect=0)
    assert abs(reflected.x - 0) < 1e-10
    assert abs(reflected.y - 1) < 1e-10
    assert reflected.z == 1

def test_reflectXYpolar_cardinal_directions():
    """Test reflection using polar angles at cardinal directions"""
    point = Point(x=2, y=3, z=1)
    origin = Point(x=0, y=0, z=0)
    
    # Reflect about x-axis (angle = 0)
    reflected = reflectXYpolar(point, origin, 0)
    assert reflected.x == 2
    assert reflected.y == -3
    assert reflected.z == 1
    
    # Reflect about y-axis (angle = pi/2)
    reflected = reflectXYpolar(point, origin, pi/2)
    assert reflected.x == -2
    assert reflected.y == 3
    assert reflected.z == 1

def test_reflectXYpolar_diagonal():
    """Test reflection using polar angles at diagonal directions"""
    point = Point(x=1, y=0, z=1)
    origin = Point(x=0, y=0, z=0)
    
    # Reflect about 45-degree line (angle = pi/4)
    reflected = reflectXYpolar(point, origin, pi/4)
    assert abs(reflected.x - 0) < 1e-10
    assert abs(reflected.y - 1) < 1e-10
    assert reflected.z == 1

def test_reflectXY_self_reflection():
    """Test reflection of a point that lies on the reflection line"""
    point = Point(x=1, y=0, z=1)
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=2, y=0, z=0)
    
    reflected = reflectXY(point, p1, p2)
    assert abs(reflected.x - point.x) < 1e-10
    assert abs(reflected.y - point.y) < 1e-10
    assert reflected.z == point.z

def test_reflectXY_z_preservation():
    """Test that z-coordinates are preserved during reflection"""
    point = Point(x=1, y=1, z=5)
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=0, z=10)  # Different z-coordinate shouldn't affect reflection
    
    reflected = reflectXY(point, p1, p2)
    assert reflected.z == 5  # Original z-coordinate should be preserved

def test_reflectXYpolar_offset_origin():
    """Test reflection about a line with non-zero origin point"""
    point = Point(x=2, y=2, z=1)
    origin = Point(x=1, y=1, z=0)
    
    # Reflect about horizontal line through (1,1)
    reflected = reflectXYpolar(point, origin, 0)
    assert abs(reflected.x - 2) < 1e-10
    assert abs(reflected.y - 0) < 1e-10
    assert reflected.z == 1

def test_reflectXY_mc_arbitrary_line():
    """Test reflection about an arbitrary line y = mx + c"""
    point = Point(x=2, y=2, z=1)
    
    # Reflect about y = 2x + 1
    reflected = reflectXY_mc(point, m_reflect=2, c_reflect=1)
    # Expected values calculated geometrically
    assert abs(reflected.x - 0) < 1e-10
    assert abs(reflected.y - 1) < 1e-10
    assert reflected.z == 1