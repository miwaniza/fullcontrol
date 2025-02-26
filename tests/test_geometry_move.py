import pytest
from fullcontrol.geometry.move import move, move_geometry, copy_geometry
from fullcontrol.combinations.gcode_and_visualize.classes import Point
from fullcontrol.geometry import Vector


def test_move_point():
    """Test move function with a Point object"""
    point = Point(x=10, y=20, z=30)
    vector = Vector(x=5, y=10, z=15)
    
    result = move(point, vector)
    
    assert isinstance(result, Point)
    assert result.x == 15
    assert result.y == 30
    assert result.z == 45
    # Original point should not be modified
    assert point.x == 10
    assert point.y == 20
    assert point.z == 30


def test_move_list():
    """Test move function with a list of Points and other objects"""
    points = [
        Point(x=10, y=20, z=30),
        "not a point",
        Point(x=15, y=25, z=35)
    ]
    vector = Vector(x=5, y=10, z=15)
    
    result = move(points, vector)
    
    assert len(result) == 3
    assert isinstance(result[0], Point)
    assert result[0].x == 15
    assert result[0].y == 30
    assert result[0].z == 45
    assert result[1] == "not a point"  # Non-Point objects should pass through
    assert isinstance(result[2], Point)
    assert result[2].x == 20
    assert result[2].y == 35
    assert result[2].z == 50
    # Original list should not be modified
    assert points[0].x == 10
    assert points[0].y == 20
    assert points[0].z == 30


def test_move_with_partial_vector():
    """Test move with a vector that has some None values"""
    point = Point(x=10, y=20, z=30)
    vector = Vector(x=5, y=None, z=15)
    
    result = move(point, vector)
    
    assert isinstance(result, Point)
    assert result.x == 15
    assert result.y == 20  # y should remain unchanged
    assert result.z == 45


def test_move_with_copy():
    """Test move with copy option"""
    point = Point(x=10, y=20, z=30)
    vector = Vector(x=5, y=10, z=15)
    
    result = move(point, vector, copy=True, copy_quantity=3)
    
    assert len(result) == 3
    assert isinstance(result[0], Point)
    assert isinstance(result[1], Point)
    assert isinstance(result[2], Point)
    
    # First copy (i=0)
    assert result[0].x == 10
    assert result[0].y == 20
    assert result[0].z == 30
    # Second copy (i=1)
    assert result[1].x == 15
    assert result[1].y == 30
    assert result[1].z == 45
    # Third copy (i=2)
    assert result[2].x == 20
    assert result[2].y == 40
    assert result[2].z == 60


def test_copy_geometry_list():
    """Test copy_geometry with a list of Points and other objects"""
    points = [
        Point(x=10, y=20, z=30),
        "not a point",
        Point(x=15, y=25, z=35)
    ]
    vector = Vector(x=5, y=10, z=15)
    
    result = copy_geometry(points, vector, 2)
    
    # With extend, we get a flat list of all elements
    assert len(result) == 6  # 2 copies of list with 3 elements
    
    # First batch (i=0)
    assert isinstance(result[0], Point)
    assert result[0].x == 10
    assert result[0].y == 20
    assert result[0].z == 30
    assert result[1] == "not a point"
    assert isinstance(result[2], Point)
    assert result[2].x == 15
    assert result[2].y == 25
    assert result[2].z == 35
    
    # Second batch (i=1)
    assert isinstance(result[3], Point)
    assert result[3].x == 15
    assert result[3].y == 30
    assert result[3].z == 45
    assert result[4] == "not a point"
    assert isinstance(result[5], Point)
    assert result[5].x == 20
    assert result[5].y == 35
    assert result[5].z == 50