import pytest
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.extrusion_classes import Extruder
from fullcontrol.common import Printer
from fullcontrol.gcode.commands import ManualGcode

def test_basic_gcode_generation():
    """Test basic G-code generation with simple movements"""
    steps = [
        Point(x=0, y=0, z=0),
        Point(x=10, y=10, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    # Basic movement should be present
    assert "G0" in result  # Travel move
    assert "X10" in result
    assert "Y10" in result

def test_gcode_with_extrusion():
    """Test G-code generation with extrusion"""
    steps = [
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=10, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    # Should contain extrusion move
    assert "G1" in result  # Extrusion move
    assert "E" in result  # Extrusion amount

def test_gcode_with_printer_settings():
    """Test G-code generation with custom printer settings"""
    steps = [
        Point(x=0, y=0, z=0),
        Printer(print_speed=1000),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "F1000" in result

def test_gcode_with_manual_commands():
    """Test G-code generation with manual G-code insertion"""
    steps = [
        Point(x=0, y=0, z=0),
        ManualGcode(text="M104 S200 ; Set temperature"),
        Point(x=10, y=0, z=0)
    ]
    controls = GcodeControls(printer_name="Community/Generic")
    result = gcode(steps, controls, show_tips=False)
    
    assert "M104 S200" in result
    assert "; Set temperature" in result

def test_gcode_save_to_file(tmp_path):
    """Test G-code saving to file"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(
        printer_name="Community/Generic",
        save_as=str(tmp_path / "test_output")
    )
    gcode(steps, controls, show_tips=False)
    
    # Check if any .gcode file was created
    gcode_files = list(tmp_path.glob("*.gcode"))
    assert len(gcode_files) > 0