
import subprocess
import sys

try:
    result = subprocess.run(
        [sys.executable, "minimal_test.py"],
        capture_output=True,
        text=True,
        cwd="c:\\github\\fullcontrol"
    )
    
    output = result.stdout
    errors = result.stderr
    
    # Write both to files we can read
    with open("c:\\github\\fullcontrol\\minimal_out.txt", "w") as f:
        f.write(output)
    
    with open("c:\\github\\fullcontrol\\minimal_err.txt", "w") as f:
        f.write(errors)
    
    print("Output written to minimal_out.txt and minimal_err.txt")
    
except Exception as e:
    with open("c:\\github\\fullcontrol\\minimal_error.txt", "w") as f:
        f.write(str(e))
