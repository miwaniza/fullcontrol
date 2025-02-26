
"""
Run our verification and the actual tests
"""
import os
import sys
import subprocess

def main():
    os.makedirs("testResults", exist_ok=True)
    
    # First run our verification script
    print("=== Running verification tests ===")
    verify_cmd = [sys.executable, "verify_fixes.py"]
    verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
    
    with open(os.path.join("testResults", "verification_output.txt"), "w") as f:
        f.write(verify_result.stdout)
        f.write("\n\n")
        f.write(verify_result.stderr)
    
    print(verify_result.stdout)
    if verify_result.stderr:
        print("STDERR:", verify_result.stderr)
    
    # Now run the actual tests
    print("\n=== Running pytest tests ===")
    pytest_cmd = [sys.executable, "-m", "pytest", "tests/test_gcode_controls.py", "-v"]
    pytest_result = subprocess.run(pytest_cmd, capture_output=True, text=True)
    
    with open(os.path.join("testResults", "pytest_output.txt"), "w") as f:
        f.write(pytest_result.stdout)
        f.write("\n\n")
        f.write(pytest_result.stderr)
    
    print(pytest_result.stdout)
    if pytest_result.stderr:
        print("STDERR:", pytest_result.stderr)
    
    # Return success only if both tests pass
    return verify_result.returncode + pytest_result.returncode

if __name__ == "__main__":
    sys.exit(main())
