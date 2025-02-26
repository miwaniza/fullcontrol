
import subprocess
import sys

try:
    print("Running direct test...")
    process = subprocess.run(
        [sys.executable, "direct_test.py"], 
        capture_output=True,
        text=True,
        cwd='c:\\github\\fullcontrol'
    )
    
    # Write output to files
    with open("c:\\github\\fullcontrol\\test_out.txt", "w") as f:
        f.write(process.stdout)
        
    with open("c:\\github\\fullcontrol\\test_err.txt", "w") as f:
        f.write(process.stderr)
        
    print("Test results written to test_out.txt and test_err.txt")
except Exception as e:
    print(f"Error running test: {e}")
    with open("c:\\github\\fullcontrol\\test_error.txt", "w") as f:
        f.write(str(e))
