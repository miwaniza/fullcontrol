
"""
Run the tests one final time to verify our fixes
"""
import subprocess
import sys
import os

def main():
    # Create testResults directory if it doesn't exist
    os.makedirs("testResults", exist_ok=True)
    
    # Run the pytest command for test_gcode_controls.py
    cmd = [sys.executable, "-m", "pytest", "tests/test_gcode_controls.py", "-v"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Save the output
    with open(os.path.join("testResults", "test_gcode_controls_final.txt"), "w") as f:
        f.write(result.stdout)
        f.write("\n\n")
        f.write(result.stderr)
    
    # Print the result
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    # Return exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
