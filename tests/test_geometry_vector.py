import pytest
import math
from fullcontrol.geometry.vector import Vector
from fullcontrol.point import Point


def test_vector_init():
    """Test Vector initialization and attribute access"""
    v = Vector(x=1, y=2, z=3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3

    # Test initialization with defaults
    v = Vector()
    assert v.x is None
    assert v.y is None
    assert v.z is None


def test_vector_from_points():
    """Test creation of a vector from two points"""
    p1 = Point(x=1, y=2, z=3)
    p2 = Point(x=4, y=6, z=8)
    
    v = Vector.from_points(p1, p2)
    
    assert v.x == 3
    assert v.y == 4
    assert v.z == 5


def test_vector_addition():
    """Test vector addition"""
    v1 = Vector(x=1, y=2, z=3)
    v2 = Vector(x=4, y=5, z=6)
    
    result = v1 + v2
    
    assert result.x == 5
    assert result.y == 7
    assert result.z == 9


def test_vector_subtraction():
    """Test vector subtraction"""
    v1 = Vector(x=4, y=6, z=8)
    v2 = Vector(x=1, y=2, z=3)
    
    result = v1 - v2
    
    assert result.x == 3
    assert result.y == 4
    assert result.z == 5


def test_vector_scalar_multiplication():
    """Test vector multiplication by a scalar"""
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


def test_vector_division():
    """Test vector division by a scalar"""
    v = Vector(x=2, y=4, z=6)
    
    result = v / 2
    
    assert result.x == 1
    assert result.y == 2
    assert result.z == 3


def test_vector_dot_product():
    """Test dot product calculation"""
    v1 = Vector(x=1, y=2, z=3)
    v2 = Vector(x=4, y=5, z=6)
    
    result = v1.dot(v2)
    
    assert result == 1*4 + 2*5 + 3*6
    assert result == 32


def test_vector_cross_product():
    """Test cross product calculation"""
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=0, y=1, z=0)
    
    result = v1.cross(v2)
    
    assert result.x == 0
    assert result.y == 0
    assert result.z == 1


def test_vector_magnitude():
    """Test magnitude calculation"""
    v = Vector(x=3, y=4, z=0)
    
    result = v.magnitude()
    
    assert result == 5
    
    v = Vector(x=1, y=1, z=1)
    
    result = v.magnitude()
    
    assert math.isclose(result, math.sqrt(3))


def test_vector_normalize():
    """Test vector normalization"""
    v = Vector(x=3, y=4, z=0)
    
    normalized = v.normalize()
    
    assert math.isclose(normalized.x, 0.6)
    assert math.isclose(normalized.y, 0.8)
    assert math.isclose(normalized.z, 0)
    assert math.isclose(normalized.magnitude(), 1)


def test_vector_angle():
    """Test angle calculation between vectors"""
    v1 = Vector(x=1, y=0, z=0)
    v2 = Vector(x=0, y=1, z=0)
    
    angle = v1.angle(v2)
    
    assert math.isclose(angle, math.pi/2)
    
    v3 = Vector(x=1, y=1, z=0)
    
    angle = v1.angle(v3)
    
    assert math.isclose(angle, math.pi/4)


def test_unit_vectors():
    """Test unit vector creation"""
    ux = Vector.unit_x()
    uy = Vector.unit_y()
    uz = Vector.unit_z()
    
    assert ux.x == 1 and ux.y == 0 and ux.z == 0
    assert uy.x == 0 and uy.y == 1 and uy.z == 0
    assert uz.x == 0 and uz.y == 0 and uz.z == 1
    
    assert math.isclose(ux.magnitude(), 1)
    assert math.isclose(uy.magnitude(), 1)
    assert math.isclose(uz.magnitude(), 1)