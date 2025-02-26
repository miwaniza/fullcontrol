
"""
Run the debug script and save the output
"""
import subprocess
import sys
import os

def main():
    # Create testResults directory if it doesn't exist
    os.makedirs("testResults", exist_ok=True)
    
    # Run the debug script
    cmd = [sys.executable, "debug_test.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Save the output
    with open(os.path.join("testResults", "debug_output.txt"), "w") as f:
        f.write(result.stdout)
        f.write("\n\n")
        f.write(result.stderr)
    
    # Print the result
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

if __name__ == "__main__":
    main()
