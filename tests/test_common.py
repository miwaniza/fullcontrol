import pytest
from fullcontrol.extra_functions import first_point, last_point, flatten, linspace, relative_point
from fullcontrol.point import Point


def test_first_point_fully_defined():
    """Test first_point with fully defined Points"""
    points = [
        "not a point",
        Point(x=10, y=None, z=30),  # Not fully defined
        Point(x=20, y=20, z=20),    # Fully defined
        Point(x=30, y=30, z=30)     # Fully defined
    ]
    
    result = first_point(points)
    
    assert result.x == 20
    assert result.y == 20
    assert result.z == 20


def test_first_point_not_fully_defined():
    """Test first_point with fully_defined=False"""
    points = [
        "not a point",
        Point(x=10, y=None, z=30),  # Not fully defined
        Point(x=20, y=20, z=20)     # Fully defined
    ]
    
    result = first_point(points, fully_defined=False)
    
    assert result.x == 10
    assert result.y is None
    assert result.z == 30


def test_first_point_no_points():
    """Test first_point with no Points in the list"""
    points = ["not a point", "still not a point"]
    
    with pytest.raises(Exception) as excinfo:
        first_point(points)
    
    assert "No point found" in str(excinfo.value)


def test_last_point_fully_defined():
    """Test last_point with fully defined Points"""
    points = [
        Point(x=10, y=10, z=10),    # Fully defined
        Point(x=20, y=20, z=20),    # Fully defined
        Point(x=30, y=None, z=30),  # Not fully defined
        "not a point"
    ]
    
    result = last_point(points)
    
    assert result.x == 20
    assert result.y == 20
    assert result.z == 20


def test_last_point_not_fully_defined():
    """Test last_point with fully_defined=False"""
    points = [
        Point(x=10, y=10, z=10),    # Fully defined
        Point(x=30, y=None, z=30),  # Not fully defined
        "not a point"
    ]
    
    result = last_point(points, fully_defined=False)
    
    assert result.x == 30
    assert result.y is None
    assert result.z == 30


def test_flatten():
    """Test flatten function"""
    nested_list = [
        1,
        [2, 3],
        4,
        [5, 6, 7],
        8
    ]
    
    result = flatten(nested_list)
    
    assert result == [1, 2, 3, 4, 5, 6, 7, 8]


def test_linspace():
    """Test linspace function"""
    result = linspace(0, 10, 5)
    
    assert len(result) == 5
    assert result[0] == 0
    assert result[1] == 2.5
    assert result[2] == 5
    assert result[3] == 7.5
    assert result[4] == 10


def test_relative_point():
    """Test relative_point function with Point"""
    reference = Point(x=10, y=20, z=30)
    
    result = relative_point(reference, 5, 10, 15)
    
    assert result.x == 15
    assert result.y == 30
    assert result.z == 45
    # Original point should not be modified
    assert reference.x == 10
    assert reference.y == 20
    assert reference.z == 30


def test_relative_point_with_list():
    """Test relative_point function with list of Points"""
    points = [
        Point(x=5, y=5, z=5),
        Point(x=10, y=20, z=30)  # Last point is used as reference
    ]
    
    result = relative_point(points, 5, 10, 15)
    
    assert result.x == 15
    assert result.y == 30
    assert result.z == 45


def test_relative_point_with_invalid_reference():
    """Test relative_point with invalid reference"""
    with pytest.raises(Exception) as excinfo:
        relative_point("not a point", 5, 10, 15)
    
    assert "must be a Point or a list" in str(excinfo.value)


def test_relative_point_with_undefined_reference():
    """Test relative_point with reference that has undefined coordinates"""
    reference = Point(x=10, y=None, z=30)
    
    with pytest.raises(Exception) as excinfo:
        relative_point(reference, 5, 10, 15)
    
    assert "must have all of x, y, z attributes defined" in str(excinfo.value)