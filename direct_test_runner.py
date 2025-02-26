
"""
A direct test runner to verify fixes for test_gcode_controls.py
"""
import sys
import inspect
import os

# Import the test functions directly from the test file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tests.test_gcode_controls import (
    test_gcode_controls_custom_start_end,
    test_gcode_controls_speed_override,
    test_gcode_controls_inheritance,
    # Also import other tests to make sure we don't break them
    test_gcode_controls_initialization,
    test_gcode_controls_with_initialization_data,
    test_gcode_controls_printer_validation,
    test_gcode_controls_save_as,
    test_gcode_controls_post_initialization
)

# List of all test functions
all_tests = [
    test_gcode_controls_initialization,
    test_gcode_controls_with_initialization_data,
    test_gcode_controls_printer_validation,
    test_gcode_controls_save_as,
    test_gcode_controls_custom_start_end,
    test_gcode_controls_speed_override,
    test_gcode_controls_post_initialization,
    test_gcode_controls_inheritance
]

def run_tests():
    # Dictionary to track results
    results = {}
    
    # Run each test
    for test in all_tests:
        test_name = test.__name__
        print(f"Running {test_name}...")
        try:
            test()
            results[test_name] = "PASS"
            print(f"  {test_name}: PASSED")
        except Exception as e:
            results[test_name] = f"FAIL: {str(e)}"
            print(f"  {test_name}: FAILED - {str(e)}")
    
    # Print summary
    print("\n=== Test Summary ===")
    all_passed = True
    for name, result in results.items():
        status = "PASS" if result == "PASS" else "FAIL"
        print(f"{name}: {status}")
        if status != "PASS":
            all_passed = False
    
    print(f"\nOverall status: {'SUCCESS' if all_passed else 'FAILURE'}")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_tests())
