
"""
Run the gcode_controls tests directly to check for failures
"""
import os
import sys
import subprocess

def main():
    print("Running gcode_controls tests...")
    
    # Run the test command
    cmd = [sys.executable, "-m", "pytest", "tests/test_gcode_controls.py", "-v"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Save the output
    with open(os.path.join("testResults", "gcode_controls_fixed.txt"), "w") as f:
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
