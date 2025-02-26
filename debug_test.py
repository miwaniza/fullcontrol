
"""
Debug specific test cases that are failing
"""
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

def debug_test_custom_start_end():
    """Debug the test_gcode_controls_custom_start_end test"""
    print("\n--- DEBUG: test_gcode_controls_custom_start_end ---")
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
    steps = [
        Point(x=10, y=10, z=0, e=1)
    ]
    
    # Generate the G-code
    result = gcode(steps, controls, show_tips=False)
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if the G1 X10 movement is in the result
    result_lines = result.splitlines()
    movement_lines = [line for line in result_lines if "G1 X10" in line]
    print(f"\nFound {len(movement_lines)} lines with 'G1 X10'")
    if movement_lines:
        print("Movement lines:", movement_lines)
    
    # Check start G-code
    has_start = (result_lines[0] == "G28 ; Custom home" and 
                 result_lines[1] == "G1 Z10 ; Raise Z")
    print("Start G-code correct:", has_start)
    
    # Check end G-code
    has_end = (result_lines[-1] == "M104 S0 ; Turn off hotend")
    print("End G-code correct:", has_end)

def debug_test_speed_override():
    """Debug the test_gcode_controls_speed_override test"""
    print("\n--- DEBUG: test_gcode_controls_speed_override ---")
    controls = GcodeControls(
        printer_name="generic",
        initialization_data={"print_speed": 1000}
    )
    
    # Create steps with printer speed override
    steps = [
        Point(x=0, y=0, z=0),
        Printer(print_speed=2000),  # Should override the initialization speed
        Point(x=10, y=0, z=0)
    ]
    
    # Generate the G-code
    result = gcode(steps, controls, show_tips=False)
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if F2000 is in the result
    has_override = "F2000" in result
    print("Contains F2000:", has_override)
    
    # Show all F values
    f_values = []
    for line in result.splitlines():
        if 'F' in line:
            f_part = line.split('F')[1].split()[0]
            f_values.append(f_part)
    
    print("F values in output:", f_values)

def debug_test_inheritance():
    """Debug the test_gcode_controls_inheritance test"""
    print("\n--- DEBUG: test_gcode_controls_inheritance ---")
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
    print("Base initialization_data:", base_controls.initialization_data)
    print("Derived initialization_data:", derived_controls.initialization_data)
    
    # Generate the G-code
    steps = [Point(x=0, y=0, z=0)]
    result = gcode(steps, derived_controls, show_tips=False)
    
    # Print the result
    print("\nGenerated G-code:")
    print(result)
    
    # Check if F1500 is in the result
    has_override = "F1500" in result
    print("Contains F1500:", has_override)
    
    # Show all F values
    f_values = []
    for line in result.splitlines():
        if 'F' in line:
            f_part = line.split('F')[1].split()[0]
            f_values.append(f_part)
    
    print("F values in output:", f_values)

if __name__ == "__main__":
    debug_test_custom_start_end()
    debug_test_speed_override()
    debug_test_inheritance()
