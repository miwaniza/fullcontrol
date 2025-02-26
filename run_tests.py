
import subprocess
import sys

try:
    result = subprocess.run(
        ['python', '-m', 'pytest', 'tests/test_gcode_controls.py', '-v'], 
        capture_output=True,
        text=True,
        cwd='c:\\github\\fullcontrol'
    )
    
    with open('test_results.txt', 'w') as f:
        f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
    
    print("Tests executed, results written to test_results.txt")
    sys.exit(result.returncode)
except Exception as e:
    with open('test_results.txt', 'w') as f:
        f.write(f"ERROR: {str(e)}")
    print(f"Error: {str(e)}")
    sys.exit(1)
