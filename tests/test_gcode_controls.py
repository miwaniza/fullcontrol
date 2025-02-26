import pytest
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

def test_gcode_controls_initialization():
    """Test basic initialization of GcodeControls"""
    controls = GcodeControls(printer_name="generic")
    assert controls.printer_name == "generic"
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
        printer_name="generic",
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
        printer_name="generic",
        save_as="test_output"
    )
    assert controls.save_as == "test_output"

def test_gcode_controls_custom_start_end():
    """Test custom start and end G-code"""
    custom_start = "G28 ; Custom home\nG1 Z10 ; Raise Z"
    custom_end = "M104 S0 ; Turn off hotend"
    controls = GcodeControls(
        printer_name="generic",
        initialization_data={
            "start_gcode": custom_start,
            "end_gcode": custom_end,
            "print_speed": 1000,
            "travel_speed": 2000,
            "extrusion_width": 0.4,
            "extrusion_height": 0.2
        }
    )
    steps = [Point(x=10, y=10, z=0, e=1)]  # Add a simple movement
    result = gcode(steps, controls, show_tips=False)
    
    result_lines = result.splitlines()
    
    # Check start G-code appears at the beginning
    assert result_lines[0] == "G28 ; Custom home"
    assert result_lines[1] == "G1 Z10 ; Raise Z"
    
    # Check end G-code appears at the end
    assert result_lines[-1] == "M104 S0 ; Turn off hotend"
    
    # Verify the actual movement command is between start and end
    movement_lines = [line for line in result_lines if "G1 X10" in line]
    assert len(movement_lines) > 0
    movement_index = result_lines.index(movement_lines[0])
    assert movement_index > 1  # After start G-code
    assert movement_index < len(result_lines) - 1  # Before end G-code

def test_gcode_controls_speed_override():
    """Test speed settings override through controls"""
    controls = GcodeControls(
        printer_name="generic",
        initialization_data={"print_speed": 1000}
    )
    steps = [
        Point(x=0, y=0, z=0),
        Printer(print_speed=2000),  # Should override the initialization speed
        Point(x=10, y=0, z=0)
    ]
    result = gcode(steps, controls, show_tips=False)
    
    assert "F2000" in result  # Should use the overridden speed

def test_gcode_controls_post_initialization():
    """Test initialization method of GcodeControls"""
    controls = GcodeControls(printer_name="generic")
    controls.initialize()
    
    # After initialization, these should be set with correct values
    assert controls.printer_name == "generic"
    assert isinstance(controls.initialization_data, dict)
    assert "print_speed" in controls.initialization_data
    assert "travel_speed" in controls.initialization_data
    assert "extrusion_width" in controls.initialization_data
    assert "extrusion_height" in controls.initialization_data

def test_gcode_controls_inheritance():
    """Test that initialization data properly inherits and overrides defaults"""
    base_controls = GcodeControls(
        printer_name="generic",
        initialization_data={"print_speed": 1000, "travel_speed": 2000}
    )
    
    # Create new controls inheriting from base but overriding print_speed
    override_data = {"print_speed": 1500}
    derived_controls = GcodeControls(
        printer_name="generic",
        initialization_data={**base_controls.initialization_data, **override_data}
    )
    
    # Use a Point with e=1 to ensure it uses print_speed instead of travel_speed
    steps = [Point(x=0, y=0, z=0, e=1)]
    result = gcode(steps, derived_controls, show_tips=False)
    
    assert "F1500" in result  # Should use the overridden print speed