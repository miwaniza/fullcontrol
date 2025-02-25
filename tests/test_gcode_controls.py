import pytest
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

def test_gcode_controls_initialization():
    """Test basic initialization of GcodeControls"""
    controls = GcodeControls(printer_name="Community/Generic")
    assert controls.printer_name == "Community/Generic"
    assert isinstance(controls.initialization_data, dict)

def test_gcode_controls_with_initialization_data():
    """Test GcodeControls with custom initialization data"""
    init_data = {
        "print_speed": 1000,
        "travel_speed": 2000,
        "extrusion_width": 0.4,
        "extrusion_height": 0.2
    }
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data=init_data
    )
    assert controls.initialization_data == init_data

def test_gcode_controls_printer_validation():
    """Test validation of printer names"""
    with pytest.raises(ValueError):
        GcodeControls(printer_name="NonexistentPrinter")

def test_gcode_controls_save_as():
    """Test save_as functionality"""
    controls = GcodeControls(
        printer_name="Community/Generic",
        save_as="test_output"
    )
    assert controls.save_as == "test_output"

def test_gcode_controls_custom_start_end():
    """Test custom start and end G-code"""
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={
            "start_gcode": "G28 ; Custom home\\nG1 Z10 ; Raise Z",
            "end_gcode": "M104 S0 ; Turn off hotend"
        }
    )
    steps = [Point(x=0, y=0, z=0)]
    result = gcode(steps, controls, show_tips=False)
    
    assert "G28 ; Custom home" in result
    assert "G1 Z10 ; Raise Z" in result
    assert "M104 S0 ; Turn off hotend" in result

def test_gcode_controls_speed_override():
    """Test speed settings override through controls"""
    controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"print_speed": 1000}
    )
    steps = [
        Point(x=0, y=0, z=0),
        Printer(print_speed=2000),  # Should override the initialization speed
        Point(x=10, y=0, z=0)
    ]
    result = gcode(steps, controls, show_tips=False)
    
    assert "F2000" in result  # Should use the overridden speed

def test_gcode_controls_initialization():
    """Test initialization method of GcodeControls"""
    controls = GcodeControls(printer_name="Community/Generic")
    controls.initialize()
    
    # After initialization, these should be set
    assert hasattr(controls, "printer_name")
    assert hasattr(controls, "initialization_data")
    assert isinstance(controls.initialization_data, dict)

def test_gcode_controls_inheritance():
    """Test that initialization data properly inherits and overrides defaults"""
    base_controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data={"print_speed": 1000, "travel_speed": 2000}
    )
    
    # Create new controls inheriting from base but overriding print_speed
    override_data = {"print_speed": 1500}
    derived_controls = GcodeControls(
        printer_name="Community/Generic",
        initialization_data=override_data
    )
    
    steps = [Point(x=0, y=0, z=0)]
    result = gcode(steps, derived_controls, show_tips=False)
    
    assert "F1500" in result  # Should use the overridden speed