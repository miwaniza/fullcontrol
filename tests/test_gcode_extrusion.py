import pytest
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.extrusion_classes import Extruder, ExtrusionGeometry

def test_relative_extrusion():
    """Test relative extrusion mode"""
    steps = [
        Extruder(relative_gcode=True),
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M83" in result  # Relative extrusion mode
    assert "G1" in result  # Extrusion move
    assert "E" in result  # Extrusion amount

def test_absolute_extrusion():
    """Test absolute extrusion mode"""
    steps = [
        Extruder(relative_gcode=False),
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=0, z=0),
        Point(x=20, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M82" in result  # Absolute extrusion mode
    assert "G92 E0" in result  # Reset extrusion distance
    assert "G1" in result

def test_extrusion_geometry_rectangular():
    """Test rectangular extrusion geometry"""
    steps = [
        ExtrusionGeometry(width=0.4, height=0.2),
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"relative_extrusion": True}
    )
    result = gcode(steps, controls, show_tips=False)
    
    assert "G1" in result
    assert "E" in result

def test_extrusion_geometry_circular():
    """Test circular extrusion geometry"""
    steps = [
        ExtrusionGeometry(diameter=0.4),
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"relative_extrusion": True}
    )
    result = gcode(steps, controls, show_tips=False)
    
    assert "G1" in result
    assert "E" in result

def test_extruder_on_off():
    """Test extruder on/off transitions"""
    steps = [
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=0, z=0),
        Extruder(on=False),
        Point(x=20, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    # Check for transitions between G1 (extrusion) and G0 (travel)
    lines = result.split('\n')
    g1_found = False
    g0_found = False
    for line in lines:
        if line.startswith('G1'):
            g1_found = True
        if line.startswith('G0'):
            g0_found = True
    
    assert g1_found and g0_found

def test_extrusion_with_retraction():
    """Test extrusion with retraction"""
    steps = [
        Point(x=0, y=0, z=0),
        Extruder(on=True, retraction=1.0),
        Point(x=10, y=0, z=0),
        Extruder(on=False),
        Point(x=20, y=0, z=0)
    ]
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"relative_extrusion": True}
    )
    result = gcode(steps, controls, show_tips=False)
    
    assert "G1 E-1" in result or "G1 E1" in result  # Retraction command