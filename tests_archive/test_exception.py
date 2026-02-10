import subprocess
import sys

try:
    print("Attempting to run a missing command...")
    subprocess.check_call(["g++", "--version"])
except Exception as e:
    print(f"Caught Exception Type: {type(e).__name__}")
    print(f"Caught Exception: {e}")
    if "FileNotFoundError" in str(type(e)):
        print("MATCHED: FileNotFoundError")
    else:
        print("MISMATCH")
