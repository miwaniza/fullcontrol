
"""
Direct test script to test the GcodeControls functionality
"""
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

def test_speed_override():
    """Test speed settings override through controls"""
    print("Testing speed override...")
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
    
    print("Generated G-code:")
    print(result)
    
    if "F2000" in result:
        print("TEST PASSED: Found F2000 in output")
    else:
        print("TEST FAILED: F2000 not found in output")
        
def test_custom_start_end():
    """Test custom start and end G-code"""
    print("\nTesting custom start and end G-code...")
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
    
    print("Generated G-code:")
    print(result)
    
    result_lines = result.splitlines()
    
    # Check start G-code appears at the beginning
    start_ok = (result_lines[0] == "G28 ; Custom home" and 
                result_lines[1] == "G1 Z10 ; Raise Z")
    
    # Check end G-code appears at the end
    end_ok = (result_lines[-1] == "M104 S0 ; Turn off hotend")
    
    if start_ok:
        print("Start G-code test PASSED")
    else:
        print("Start G-code test FAILED")
        
    if end_ok:
        print("End G-code test PASSED")
    else:
        print("End G-code test FAILED")

def test_post_initialization():
    """Test initialization method of GcodeControls"""
    print("\nTesting post-initialization...")
    controls = GcodeControls(printer_name="generic")
    controls.initialize()
    
    print("initialization_data after initialize():")
    for key, value in controls.initialization_data.items():
        print(f"  {key}: {value}")
    
    # After initialization, these should be set with correct values
    keys_to_check = ['print_speed', 'travel_speed', 'extrusion_width', 'extrusion_height']
    all_keys_present = all(key in controls.initialization_data for key in keys_to_check)
    
    if all_keys_present:
        print("Post-initialization test PASSED")
    else:
        print("Post-initialization test FAILED - missing keys:", 
              [key for key in keys_to_check if key not in controls.initialization_data])

if __name__ == "__main__":
    test_speed_override()
    test_custom_start_end() 
    test_post_initialization()
    
    print("\nAll tests completed.")
