import pytest
from fullcontrol.gcode.tips import tips
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from io import StringIO
import sys

def test_extrusion_width_height_tip():
    """Test tip generation for missing extrusion width/height"""
    controls = GcodeControls(printer_name="Community/Generic")
    
    # Capture stdout to check tip message
    stdout = StringIO()
    sys.stdout = stdout
    
    tips(controls)
    output = stdout.getvalue()
    sys.stdout = sys.__stdout__
    
    assert "extrusion_width" in output
    assert "extrusion_height" in output

def test_no_tips_with_complete_config():
    """Test that no tips are shown when all required parameters are set"""
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={
            "extrusion_width": 0.4,
            "extrusion_height": 0.2
        }
    )
    
    stdout = StringIO()
    sys.stdout = stdout
    
    tips(controls)
    output = stdout.getvalue()
    sys.stdout = sys.__stdout__
    
    assert output.strip() == ""

def test_tip_suppression():
    """Test that tips can be suppressed with show_tips=False"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(printer_name="Community/Generic")
    
    stdout = StringIO()
    sys.stdout = stdout
    
    gcode(steps, controls, show_tips=False)
    output = stdout.getvalue()
    sys.stdout = sys.__stdout__
    
    assert "tip:" not in output

def test_tips_display():
    """Test that tips are shown by default"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(printer_name="Community/Generic")
    
    stdout = StringIO()
    sys.stdout = stdout
    
    gcode(steps, controls, show_tips=True)
    output = stdout.getvalue()
    sys.stdout = sys.__stdout__
    
    assert "tip:" in output

def test_tips_with_partial_config():
    """Test tips when only some parameters are configured"""
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"extrusion_width": 0.4}  # Missing height
    )
    
    stdout = StringIO()
    sys.stdout = stdout
    
    tips(controls)
    output = stdout.getvalue()
    sys.stdout = sys.__stdout__
    
    assert "extrusion_height" in output
    assert "extrusion_width" not in output  # Should not mention width since it's set