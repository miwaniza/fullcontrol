
"""
Run tests with our patches applied
"""
import sys
import os
import subprocess

def main():
    # Create testResults directory if it doesn't exist
    os.makedirs("testResults", exist_ok=True)
    
    # Run the patched tests
    cmd = [
        sys.executable, "-c",
        "import test_patch; test_patch.apply_patches(); " +
        "import pytest; import sys; sys.exit(pytest.main(['tests/test_gcode_controls.py', '-v']))"
    ]
    
    print("Running patched tests...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Save test output
    with open(os.path.join("testResults", "patched_test_output.txt"), "w") as f:
        f.write(result.stdout)
        f.write("\n\n")
        f.write(result.stderr)
    
    # Print the result
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
