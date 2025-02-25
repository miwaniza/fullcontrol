import pytest
from math import sqrt, pi
from fullcontrol.geometry import Point
from fullcontrol.geometry.vector import Vector

def test_vector_initialization():
    # Test empty initialization
    v = Vector()
    assert v.x is None
    assert v.y is None
    assert v.z is None
    
    # Test full initialization
    v = Vector(x=1.0, y=2.0, z=3.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
    
    # Test partial initialization
    v = Vector(x=1.0, y=2.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z is None

def test_vector_updates():
    v = Vector()
    
    # Test setting values
    v.x = 1.0
    v.y = 2.0
    v.z = 3.0
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
    
    # Test updating values
    v.x = 4.0
    assert v.x == 4.0

def test_vector_validation():
    # Test invalid x value
    with pytest.raises(Exception):
        Vector(x="not a number", y=1.0, z=1.0)
    
    # Test invalid y value
    with pytest.raises(Exception):
        Vector(x=1.0, y="not a number", z=1.0)
    
    # Test invalid z value
    with pytest.raises(Exception):
        Vector(x=1.0, y=1.0, z="not a number")

def test_vector_creation():
    """Test basic vector creation and attributes"""
    v = Vector(x=1, y=2, z=3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3
    
    # Test creation with None values
    v = Vector(x=1, y=None, z=3)
    assert v.x == 1
    assert v.y is None
    assert v.z == 3

def test_vector_from_points():
    """Test vector creation from two points"""
    p1 = Point(x=0, y=0, z=0)
    p2 = Point(x=1, y=2, z=3)
    v = Vector.from_points(p1, p2)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3
    
    # Test with None values
    p3 = Point(x=2, y=None, z=4)
    v = Vector.from_points(p1, p3)
    assert v.x == 2
    assert v.y is None
    assert v.z == 4

def test_vector_copy():
    """Test vector copying"""
    v1 = Vector(x=1, y=2, z=3)
    v2 = v1.model_copy()
    assert v1 is not v2  # Should be a new object
    assert v1.x == v2.x
    assert v1.y == v2.y
    assert v1.z == v2.z

def test_vector_addition():
    """Test vector addition"""
    v1 = Vector(x=1, y=2, z=3)
    v2 = Vector(x=4, y=5, z=6)
    result = v1 + v2
    assert result.x == 5
    assert result.y == 7
    assert result.z == 9
    
    # Test addition with None values
    v3 = Vector(x=1, y=None, z=3)
    v4 = Vector(x=2, y=4, z=None)
    result = v3 + v4
    assert result.x == 3
    assert result.y is None
    assert result.z is None

def test_vector_subtraction():
    """Test vector subtraction"""
    v1 = Vector(x=4, y=5, z=6)
    v2 = Vector(x=1, y=2, z=3)
    result = v1 - v2
    assert result.x == 3
    assert result.y == 3
    assert result.z == 3
    
    # Test subtraction with None values
    v3 = Vector(x=1, y=None, z=3)
    v4 = Vector(x=2, y=4, z=None)
    result = v3 - v4
    assert result.x == -1
    assert result.y is None
    assert result.z is None

def test_vector_multiplication():
    """Test vector multiplication by scalar"""
    v = Vector(x=1, y=2, z=3)
    result = v * 2
    assert result.x == 2
    assert result.y == 4
    assert result.z == 6
    
    # Test right multiplication
    result = 3 * v
    assert result.x == 3
    assert result.y == 6
    assert result.z == 9
    
    # Test multiplication with None values
    v = Vector(x=1, y=None, z=3)
    result = v * 2
    assert result.x == 2
    assert result.y is None
    assert result.z == 6

def test_vector_division():
    """Test vector division by scalar"""
    v = Vector(x=2, y=4, z=6)
    result = v / 2
    assert result.x == 1
    assert result.y == 2
    assert result.z == 3
    
    # Test division with None values
    v = Vector(x=2, y=None, z=6)
    result = v / 2
    assert result.x == 1
    assert result.y is None
    assert result.z == 3

def test_vector_dot_product():
    """Test vector dot product"""
    v1 = Vector(x=1, y=2, z=3)
    v2 = Vector(x=4, y=5, z=6)
    result = v1.dot(v2)
    assert result == 32  # 1*4 + 2*5 + 3*6
    
    # Test dot product with perpendicular vectors
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=0, y=1, z=0)
    assert v1.dot(v2) == 0

def test_vector_cross_product():
    """Test vector cross product"""
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=0, y=1, z=0)
    result = v1.cross(v2)
    assert result.x == 0
    assert result.y == 0
    assert result.z == 1

def test_vector_magnitude():
    """Test vector magnitude calculation"""
    # Unit vectors
    v = Vector(x=1, y=0, z=0)
    assert v.magnitude() == 1
    
    # 3-4-5 triangle in xy plane
    v = Vector(x=3, y=4, z=0)
    assert v.magnitude() == 5
    
    # General case
    v = Vector(x=2, y=2, z=1)
    assert abs(v.magnitude() - 3) < 1e-10

def test_vector_normalize():
    """Test vector normalization"""
    v = Vector(x=3, y=4, z=0)
    normalized = v.normalize()
    assert abs(normalized.magnitude() - 1) < 1e-10
    assert abs(normalized.x - 0.6) < 1e-10  # 3/5
    assert abs(normalized.y - 0.8) < 1e-10  # 4/5
    assert abs(normalized.z) < 1e-10

def test_vector_angle():
    """Test vector angle calculation"""
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=0, y=1, z=0)
    assert abs(v1.angle(v2) - pi/2) < 1e-10  # 90 degrees
    
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=1, y=1, z=0)
    assert abs(v1.angle(v2) - pi/4) < 1e-10  # 45 degrees

def test_vector_unit_vectors():
    """Test unit vector properties"""
    # X unit vector
    v = Vector.unit_x()
    assert v.x == 1
    assert v.y == 0
    assert v.z == 0
    assert v.magnitude() == 1
    
    # Y unit vector
    v = Vector.unit_y()
    assert v.x == 0
    assert v.y == 1
    assert v.z == 0
    assert v.magnitude() == 1
    
    # Z unit vector
    v = Vector.unit_z()
    assert v.x == 0
    assert v.y == 0
    assert v.z == 1
    assert v.magnitude() == 1