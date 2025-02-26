
# Just test the critical functionality
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.steps2gcode import gcode
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer

# Test speed override
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

# Print just the relevant information
print("\nDoes result contain F2000?", "F2000" in result)

# Test the initialization
print("\nTesting post-initialization...")
controls = GcodeControls(printer_name="generic")
controls.initialize()

# Check if key values are present after initialization
keys_to_check = ['print_speed', 'travel_speed', 'extrusion_width', 'extrusion_height']
for key in keys_to_check:
    print(f"{key} in initialization_data:", key in controls.initialization_data)

# Print the entire result for debugging
print("\nFull G-code output from speed test:\n", result)
