import pytest
from fullcontrol.gcode.state import State
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer
from fullcontrol.gcode.extrusion_classes import Extruder, ExtrusionGeometry

def test_state_initialization():
    """Test basic state initialization"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(printer_name="generic")
    state = State(steps, controls)
    
    # Check that our input steps are included in state steps
    found = False
    for i in range(len(state.steps) - len(steps) + 1):
        if state.steps[i:i+len(steps)] == steps:
            found = True
            break
    assert found, "Input steps were not found as a contiguous sequence in state.steps"

    assert isinstance(state.point, Point)
    assert isinstance(state.printer, Printer)
    assert isinstance(state.extruder, Extruder)
    assert isinstance(state.extrusion_geometry, ExtrusionGeometry)

def test_state_step_processing():
    """Test state processing of steps"""
    steps = [
        Point(x=0, y=0, z=0),
        Extruder(on=True),
        Point(x=10, y=10, z=0)
    ]
    controls = GcodeControls(printer_name="generic")
    state = State(steps, controls)
    
    assert state.i == 0
    assert isinstance(state.gcode, list)
    assert len(state.gcode) == 0

def test_state_printer_initialization():
    """Test printer initialization in state"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(
        printer_name="generic",
        initialization_data={"print_speed": 1000, "travel_speed": 2000}
    )
    state = State(steps, controls)
    
    assert state.printer.print_speed == 1000
    assert state.printer.travel_speed == 2000

def test_state_extruder_initialization():
    """Test extruder initialization in state"""
    steps = [Point(x=0, y=0, z=0)]
    controls = GcodeControls(
        printer_name="generic",
        initialization_data={"relative_extrusion": True}
    )
    state = State(steps, controls)
    
    assert state.extruder.relative_gcode is True

def test_state_invalid_printer():
    """Test state initialization with invalid printer name"""
    steps = [Point(x=0, y=0, z=0)]
    
    with pytest.raises(Exception) as exc_info:
        controls = GcodeControls(printer_name="NonexistentPrinter")
        State(steps, controls)  # This line won't be reached due to validation error
    
    error_message = str(exc_info.value).lower()
    assert "printer_name" in error_message
    assert "invalid" in error_message