
import subprocess
import sys

test_file = "tests/test_gcode_controls.py"

try:
    print(f"Running pytest for {test_file}...")
    result = subprocess.run(
        ['python', '-m', 'pytest', test_file, '-v'], 
        capture_output=True,
        text=True,
        cwd='c:\\github\\fullcontrol'
    )
    
    print("\nSTDOUT:")
    print(result.stdout)
    
    print("\nSTDERR:")
    print(result.stderr)
    
    with open('test_results.txt', 'w') as f:
        f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
    
    print(f"\nTest return code: {result.returncode}")
    print(f"Results also written to test_results.txt")
    
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error running tests: {str(e)}")
    with open('test_results.txt', 'w') as f:
        f.write(f"ERROR: {str(e)}")
    sys.exit(1)
