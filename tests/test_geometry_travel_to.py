import pytest
from fullcontrol.geometry.travel_to import travel_to
from fullcontrol.extrusion_classes import Extruder
from fullcontrol.point import Point
from fullcontrol.combinations.gcode_and_visualize.classes import Point as GVPoint, Extruder as GVExtruder


def test_travel_to_point():
    """Test travel_to with a Point object"""
    point = GVPoint(x=10, y=20, z=30)
    result = travel_to(point)
    
    assert len(result) == 3
    assert isinstance(result[0], GVExtruder)
    assert isinstance(result[1], GVPoint)
    assert isinstance(result[2], GVExtruder)
    assert result[0].on is False
    assert result[1].x == 10
    assert result[1].y == 20
    assert result[1].z == 30
    assert result[2].on is True


def test_travel_to_list():
    """Test travel_to with a list of Points"""
    points = [
        GVPoint(x=10, y=20, z=30),
        GVPoint(x=15, y=25, z=35)
    ]
    result = travel_to(points)
    
    assert len(result) == 3
    assert isinstance(result[0], GVExtruder)
    assert isinstance(result[1], GVPoint)
    assert isinstance(result[2], GVExtruder)
    assert result[0].on is False
    assert result[1].x == 10
    assert result[1].y == 20
    assert result[1].z == 30
    assert result[2].on is True


def test_travel_to_invalid_type():
    """Test travel_to with invalid input type"""
    with pytest.raises(Exception) as excinfo:
        travel_to("not a point or list")
    
    assert "must be supplied" in str(excinfo.value)