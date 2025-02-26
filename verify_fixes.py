
"""
Verify our fixes for test_gcode_controls tests
"""
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

def test_custom_start_end():
    """Test custom start and end G-code"""
    print("\n--- Testing custom start and end G-code ---")
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
    
    # Create a point with explicit e=1 to ensure extrusion
    steps = [Point(x=10, y=10, z=0, e=1)]
    
    # Generate the G-code
    result = gcode(steps, controls, show_tips=False)
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if the G1 X10 movement is in the result
    result_lines = result.splitlines()
    
    # Check for specific test requirements
    has_g1_x10 = any("G1" in line and "X10" in line for line in result_lines)
    has_start = (result_lines[0] == "G28 ; Custom home" and result_lines[1] == "G1 Z10 ; Raise Z")
    has_end = (result_lines[-1] == "M104 S0 ; Turn off hotend")
    
    print(f"Has G1 X10 movement: {has_g1_x10}")
    print(f"Has correct start G-code: {has_start}")
    print(f"Has correct end G-code: {has_end}")
    
    if has_g1_x10 and has_start and has_end:
        print("TEST PASSED: test_custom_start_end")
    else:
        print("TEST FAILED: test_custom_start_end")

def test_speed_override():
    """Test speed settings override through controls"""
    print("\n--- Testing speed override ---")
    
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
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if F2000 appears in the output (indicating speed override)
    has_f2000 = "F2000" in result
    
    print(f"Has F2000 in output: {has_f2000}")
    
    if has_f2000:
        print("TEST PASSED: test_speed_override")
    else:
        print("TEST FAILED: test_speed_override")

def test_inheritance():
    """Test that initialization data properly inherits and overrides defaults"""
    print("\n--- Testing inheritance ---")
    
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
    
    # Print the initialization_data to verify
    print(f"Base initialization_data print_speed: {base_controls.initialization_data.get('print_speed')}")
    print(f"Derived initialization_data print_speed: {derived_controls.initialization_data.get('print_speed')}")
    
    # Generate the G-code with a simple point
    steps = [Point(x=0, y=0, z=0)]
    result = gcode(steps, derived_controls, show_tips=False)
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if F1500 appears in the output (indicating correct inheritance)
    has_f1500 = "F1500" in result
    
    print(f"Has F1500 in output: {has_f1500}")
    
    if has_f1500:
        print("TEST PASSED: test_inheritance")
    else:
        print("TEST FAILED: test_inheritance")

if __name__ == "__main__":
    test_custom_start_end()
    test_speed_override()
    test_inheritance()
