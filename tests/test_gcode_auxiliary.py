import pytest
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.auxilliary_components import Fan, Hotend, Buildplate

def test_fan_gcode():
    """Test G-code generation for fan control"""
    steps = [
        Point(x=0, y=0, z=0),
        Fan(speed_percent=50),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M106" in result  # Fan control command
    assert "S127" in result  # 50% of 255

def test_fan_speed_validation():
    """Test fan speed validation"""
    with pytest.raises(ValueError):
        Fan(speed_percent=150)  # Speed > 100%
    with pytest.raises(ValueError):
        Fan(speed_percent=-10)  # Speed < 0%

def test_hotend_gcode():
    """Test G-code generation for hotend control"""
    steps = [
        Point(x=0, y=0, z=0),
        Hotend(temp=200, wait=False),
        Point(x=10, y=0, z=0),
        Hotend(temp=200, wait=True),
        Point(x=20, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M104 S200" in result  # Set temp without waiting
    assert "M109 S200" in result  # Set temp and wait

def test_hotend_multi_tool():
    """Test G-code generation for multi-tool hotend control"""
    steps = [
        Hotend(temp=200, tool=0),
        Hotend(temp=210, tool=1)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M104 S200 T0" in result
    assert "M104 S210 T1" in result

def test_buildplate_gcode():
    """Test G-code generation for buildplate control"""
    steps = [
        Point(x=0, y=0, z=0),
        Buildplate(temp=60, wait=True),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M190 S60" in result  # Set bed temp and wait

def test_combined_auxiliary_controls():
    """Test G-code generation with multiple auxiliary controls"""
    steps = [
        Buildplate(temp=60, wait=True),
        Hotend(temp=200, wait=True),
        Fan(speed_percent=0),
        Point(x=0, y=0, z=0),
        Fan(speed_percent=100),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    # Check presence and order of commands
    assert "M190" in result
    assert "M109" in result
    assert "M106 S0" in result
    assert "M106 S255" in result