
"""
A direct test to verify our fixes
"""
import pytest
import sys

# Run the test_gcode_controls directly
try:
    # Import the test module
    from tests.test_gcode_controls import (
        test_gcode_controls_custom_start_end,
        test_gcode_controls_speed_override,
        test_gcode_controls_inheritance
    )
    
    # Run the tests directly
    print("Running test_gcode_controls_custom_start_end...")
    test_gcode_controls_custom_start_end()
    print("PASSED!")
    
    print("\nRunning test_gcode_controls_speed_override...")
    test_gcode_controls_speed_override()
    print("PASSED!")
    
    print("\nRunning test_gcode_controls_inheritance...")
    test_gcode_controls_inheritance()
    print("PASSED!")
    
    print("\nAll tests passed!")
    
except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)
